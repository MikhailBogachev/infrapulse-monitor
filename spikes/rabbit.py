"""Exercise broker and prefork delivery semantics with isolated synthetic messages."""

import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from uuid import uuid4

import pika
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from infrapulse.config import Settings
from infrapulse.database import make_sync_sessions
from kombu import Exchange, Producer, Queue
from sqlalchemy import text

settings = Settings.load()
fixture = os.environ.setdefault("INFRAPULSE_RABBIT_FIXTURE", uuid4().hex)
SOURCE = f"ip007.delivery.{fixture}"
DEAD = f"ip007.dead.{fixture}"
exchange = Exchange(f"ip007.work.{fixture}", type="direct", durable=True)
work = Queue(
    SOURCE,
    exchange,
    routing_key=SOURCE,
    durable=True,
    queue_arguments={
        "x-queue-type": "quorum",
        "x-delivery-limit": 3,
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": DEAD,
    },
)
app = Celery("ip007.rabbit", broker=settings.broker_url)
app.conf.update(
    broker_transport_options={"confirm_publish": True},
    task_default_queue=SOURCE,
    task_queues=(work,),
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_ignore_result=True,
    worker_prefetch_multiplier=1,
    worker_enable_remote_control=False,
    accept_content=["json"],
)
MARKERS = Path("/tmp")


def kill_once(key: str, stage: str) -> None:
    try:
        (MARKERS / f"{key}-{stage}").touch(exist_ok=False)
    except FileExistsError:
        return
    os.kill(os.getpid(), signal.SIGKILL)


@app.task(name="ip007.effect")
def effect(key: str, failure: str) -> None:
    engine, sessions = make_sync_sessions(settings)
    try:
        with sessions.begin() as session:
            session.execute(
                text("INSERT INTO ip007_effects (id) VALUES (:id) ON CONFLICT DO NOTHING"),
                {"id": key},
            )
            if failure == "precommit":
                kill_once(key, failure)
        if failure == "postcommit":
            kill_once(key, failure)
        (MARKERS / f"{key}-{failure}-done").touch()
    finally:
        engine.dispose()


@app.task(name="ip007.time_limit", acks_late=False, soft_time_limit=1, time_limit=2)
def time_limit(key: str) -> None:
    try:
        time.sleep(15)
    except SoftTimeLimitExceeded:
        (MARKERS / f"{key}-soft").write_text(str(os.getpid()))
        time.sleep(15)
    (MARKERS / f"{key}-unexpected-return").touch()


def publish_then_crash(key: str) -> None:
    app.send_task("ip007.effect", args=[key, "first-publish"], task_id=key, mandatory=True)
    (MARKERS / f"{key}-confirmed").touch()
    os.kill(os.getpid(), signal.SIGKILL)


def until(condition: Callable[[], bool], timeout: float = 20) -> None:
    end = time.monotonic() + timeout
    while not condition():
        if time.monotonic() >= end:
            raise AssertionError("Expected broker/worker evidence did not arrive")
        time.sleep(0.1)


def main() -> None:
    params = pika.URLParameters(settings.broker_url)
    params.virtual_host = "/"
    params.socket_timeout = 3
    params.blocked_connection_timeout = 3
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    worker = None
    engine, sessions = make_sync_sessions(settings)
    keys: list[str] = []
    try:
        channel.queue_declare(DEAD, durable=True)
        with app.connection_for_write() as kombu, kombu.channel() as transport:
            work(transport).declare()
            returns = []
            producer = Producer(
                transport,
                exchange=exchange,
                on_return=lambda *args: returns.append(args),
            )
            producer.publish(
                {"fixture": "unroutable"},
                routing_key="ip007.absent",
                mandatory=True,
                retry=False,
            )
            assert len(returns) == 1
            print("Kombu confirm returned an unroutable mandatory publication")
        channel.confirm_delivery()
        try:
            channel.basic_publish(exchange.name, "ip007.absent", b"fixture", mandatory=True)
        except pika.exceptions.UnroutableError:
            print("Broker acknowledged mandatory publication with a routing return")
        else:
            raise AssertionError("Expected mandatory routing failure")

        channel.basic_publish(
            exchange.name,
            SOURCE,
            b"bounded-fixture",
            properties=pika.BasicProperties(delivery_mode=2),
            mandatory=True,
        )
        observed: list[int] = []
        for _ in range(6):
            message = None

            def receive() -> bool:
                nonlocal message
                method, properties, body = channel.basic_get(SOURCE)
                if method is not None:
                    message = (method, properties, body)
                    return True
                return channel.queue_declare(DEAD, passive=True).method.message_count > 0

            until(receive)
            if message is None:
                break
            method, properties, body = message
            assert body == b"bounded-fixture"
            observed.append((properties.headers or {}).get("x-delivery-count", 0))
            channel.basic_reject(method.delivery_tag, requeue=True)
        method, properties, body = channel.basic_get(DEAD, auto_ack=True)
        assert method is not None and body == b"bounded-fixture"
        assert observed == list(range(len(observed))) and 3 <= len(observed) <= 5
        assert any(entry["reason"] == "delivery_limit" for entry in properties.headers["x-death"])
        print(f"Quorum delivery counts {observed}, then delivery_limit dead letter")

        worker = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "rabbit:app",
                "worker",
                "--concurrency=2",
                "-Q",
                SOURCE,
                "--loglevel=WARNING",
            ],
            start_new_session=True,
        )
        key = str(uuid4())
        keys.append(key)
        with sessions.begin() as session:
            session.execute(text("INSERT INTO ip007_outbox (id) VALUES (:id)"), {"id": key})
        crashed = subprocess.run(
            [sys.executable, __file__, "publish", key], check=False, timeout=10
        )
        assert crashed.returncode == -signal.SIGKILL
        assert (MARKERS / f"{key}-confirmed").exists()
        with sessions.begin() as session:
            assert (
                session.scalar(
                    text("SELECT published FROM ip007_outbox WHERE id = :id"), {"id": key}
                )
                is False
            )
            app.send_task("ip007.effect", args=[key, "relay"], task_id=key, mandatory=True)
            session.execute(
                text("UPDATE ip007_outbox SET published = true WHERE id = :id"), {"id": key}
            )
        until((MARKERS / f"{key}-first-publish-done").exists)
        until((MARKERS / f"{key}-relay-done").exists)
        with sessions() as session:
            assert (
                session.scalar(
                    text("SELECT count(*) FROM ip007_effects WHERE id = :id"), {"id": key}
                )
                == 1
            )
        print("Relay replayed a confirmed publication after publisher SIGKILL before settlement")

        for stage in ("precommit", "postcommit"):
            key = str(uuid4())
            keys.append(key)
            app.send_task("ip007.effect", args=[key, stage])
            done = MARKERS / f"{key}-{stage}-done"
            until(done.exists)
            assert (MARKERS / f"{key}-{stage}").exists()
            app.send_task("ip007.effect", args=[key, "duplicate"])
            duplicate_done = MARKERS / f"{key}-duplicate-done"
            until(duplicate_done.exists)
            with sessions() as session:
                assert (
                    session.scalar(
                        text("SELECT count(*) FROM ip007_effects WHERE id = :id"), {"id": key}
                    )
                    == 1
                )
            print(f"Prefork child SIGKILL at {stage}: redelivery completed with one DB row")

        key = str(uuid4())
        app.send_task("ip007.time_limit", args=[key])
        evidence = MARKERS / f"{key}-soft"
        until(lambda: evidence.exists() and bool(evidence.read_text()))
        timed_out_pid = int(evidence.read_text())
        until(lambda: not Path(f"/proc/{timed_out_pid}").exists(), timeout=8)
        assert not (MARKERS / f"{key}-unexpected-return").exists()
        key_after_limit = str(uuid4())
        keys.append(key_after_limit)
        app.send_task("ip007.effect", args=[key_after_limit, "after-timeout"])
        until((MARKERS / f"{key_after_limit}-after-timeout-done").exists)
        print("Soft timeout was observed and prefork remained functional after the hard deadline")
    finally:
        if worker is not None:
            worker.terminate()
            try:
                worker.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(worker.pid, signal.SIGKILL)
                worker.wait()
        with sessions.begin() as session:
            for key in keys:
                session.execute(text("DELETE FROM ip007_effects WHERE id = :id"), {"id": key})
                session.execute(text("DELETE FROM ip007_outbox WHERE id = :id"), {"id": key})
        engine.dispose()
        with suppress(pika.exceptions.AMQPError):
            channel.queue_delete(SOURCE)
            channel.queue_delete(DEAD)
            channel.exchange_delete(exchange.name)
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "publish":
        publish_then_crash(sys.argv[2])
    else:
        main()
