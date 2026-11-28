import logging
import logging.config
import sys
from typing import Any
from uuid import UUID

import structlog

SAFE_EVENTS = frozenset(
    {"readiness_failed", "scheduler_child_exited", "scheduler_shutdown", "smoke_completed"}
)


def safe_fields(
    logger: Any, method: str, event: structlog.types.EventDict
) -> structlog.types.EventDict:
    value = event.get("event")
    name = value if isinstance(value, str) and value in SAFE_EVENTS else "runtime_event"
    fields = {"event": name}
    level = event.get("level")
    if isinstance(level, str) and level in {"debug", "info", "warning", "error", "critical"}:
        fields["level"] = level
    if fields["event"] == "smoke_completed":
        task_id = event.get("task_id")
        if isinstance(task_id, str):
            try:
                fields["task_id"] = str(UUID(task_id))
            except ValueError:
                pass
    return fields


def configure_logging(level: str) -> None:
    logging.raiseExceptions = False
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "safe_json",
                }
            },
            "formatters": {
                "safe_json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "foreign_pre_chain": [structlog.stdlib.add_log_level],
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        safe_fields,
                        structlog.processors.TimeStamper(fmt="iso", utc=True),
                        structlog.processors.JSONRenderer(),
                    ],
                    "keep_exc_info": False,
                    "keep_stack_info": False,
                }
            },
            "root": {"handlers": ["stdout"], "level": level},
        }
    )
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "celery", "celery.task"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def main() -> None:
    from uvicorn import run

    from infrapulse.config import Settings

    try:
        settings = Settings.load()
        _ = settings.database_url, settings.redis_url
    except RuntimeError:
        sys.exit("Invalid InfraPulse API configuration")
    configure_logging(settings.log_level)
    run(
        "infrapulse.api:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        access_log=False,
        proxy_headers=False,
        log_config=None,
    )
