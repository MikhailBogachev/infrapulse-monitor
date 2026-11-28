import asyncio
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager
from typing import cast

import structlog
from fastapi import FastAPI, Response
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from infrapulse.config import Settings
from infrapulse.database import SCHEMA_HEAD, make_async_sessions

log = structlog.get_logger()


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings.load()
    engine, sessions = make_async_sessions(config)
    cache = Redis.from_url(
        config.redis_url,
        socket_connect_timeout=config.readiness_timeout,
        socket_timeout=config.readiness_timeout,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.sessions = sessions
        try:
            yield
        finally:
            try:
                await cache.aclose()
            finally:
                await engine.dispose()

    app = FastAPI(title="InfraPulse", lifespan=lifespan)

    @app.get("/health/live")
    async def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready", responses={503: {"description": "Required services unavailable"}})
    async def ready(response: Response) -> dict[str, str]:
        response.headers["Cache-Control"] = "no-store"
        try:
            async with asyncio.timeout(config.readiness_timeout), sessions() as session:
                versions = (
                    await session.scalars(text("SELECT version_num FROM alembic_version"))
                ).all()
                if versions == [SCHEMA_HEAD] and await cast("Awaitable[bool]", cache.ping()):
                    return {"status": "ready"}
        except (SQLAlchemyError, RedisError, TimeoutError, OSError):
            pass
        log.warning("readiness_failed")
        response.status_code = 503
        return {"status": "not_ready"}

    return app
