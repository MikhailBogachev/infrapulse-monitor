import os
from pathlib import Path
from typing import Any

import structlog
from celery import Celery, Task, signals
from kombu.entity import Exchange, Queue
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session, sessionmaker

from infrapulse.config import Settings
from infrapulse.database import make_sync_sessions
from infrapulse.logging import configure_logging

QUEUES = ("check", "notification", "control")
DEAD_EXCHANGE = Exchange("infrapulse.dead", type="direct", durable=True)
WORK_EXCHANGE = Exchange("infrapulse.work", type="direct", durable=True)
settings = Settings.load()
app = Celery("infrapulse", broker=settings.broker_url)
log = structlog.get_logger()
engine: Engine | None = None
sessions: sessionmaker[Session] | None = None
ready_file = Path(os.getenv("INFRAPULSE_WORKER_READY_FILE", "/tmp/infrapulse-worker.ready"))


def work_queue(name: str) -> Queue:
    return Queue(
        name,
        WORK_EXCHANGE,
        routing_key=name,
        durable=True,
        queue_arguments={
            "x-queue-type": "quorum",
            "x-delivery-limit": 3,
            "x-dead-letter-exchange": DEAD_EXCHANGE.name,
            "x-dead-letter-routing-key": name,
        },
    )


def dead_queue(name: str) -> Queue:
    return Queue(f"{name}.dead", DEAD_EXCHANGE, routing_key=name, durable=True)


app.conf.update(
    task_queues=tuple(work_queue(name) for name in QUEUES),
    task_routes={f"infrapulse.smoke.{name}": {"queue": name} for name in QUEUES},
    task_default_queue="control",
    task_create_missing_queues=False,
    broker_transport_options={"confirm_publish": True},
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=5,
    worker_prefetch_multiplier=1,
    worker_detect_quorum_queues=True,
    worker_enable_remote_control=False,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    accept_content=["json"],
    task_serializer="json",
    task_ignore_result=True,
    task_soft_time_limit=8,
    task_time_limit=12,
    worker_hijack_root_logger=False,
    beat_schedule={
        "control-smoke": {
            "task": "infrapulse.smoke.control",
            "schedule": 10.0,
            "options": {"expires": 20},
        }
    },
)


@signals.setup_logging.connect
def setup_logging(**kwargs: Any) -> None:
    configure_logging(settings.log_level)


@signals.worker_ready.connect
def mark_ready(**kwargs: Any) -> None:
    ready_file.touch()


@signals.worker_shutdown.connect
def clear_ready(**kwargs: Any) -> None:
    ready_file.unlink(missing_ok=True)


@signals.worker_process_init.connect
def initialize_child(**kwargs: Any) -> None:
    global engine, sessions
    engine, sessions = make_sync_sessions(settings)


@signals.worker_process_shutdown.connect
def dispose_child(**kwargs: Any) -> None:
    global engine, sessions
    if engine is not None:
        engine.dispose()
    engine, sessions = None, None


def smoke_database(task: Task) -> None:
    if sessions is None:
        raise RuntimeError("Worker database sessions are unavailable")
    with sessions() as session:
        session.execute(text("SELECT 1"))
    log.info("smoke_completed", task_id=task.request.id)


for lane in QUEUES:
    app.task(name=f"infrapulse.smoke.{lane}", bind=True)(smoke_database)


def declare_topology() -> None:
    configure_logging(settings.log_level)
    with app.connection_for_write() as connection, connection.channel() as channel:
        for name in QUEUES:
            dead_queue(name)(channel).declare()
            work_queue(name)(channel).declare()


if __name__ == "__main__":
    declare_topology()
