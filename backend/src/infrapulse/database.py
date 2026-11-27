from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from infrapulse.config import Settings

SCHEMA_HEAD = "0001_foundation"


def make_async_sessions(settings: Settings) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        settings.database_url, pool_pre_ping=True, hide_parameters=True, pool_timeout=2
    )
    return engine, async_sessionmaker(engine, expire_on_commit=False)


def make_sync_sessions(settings: Settings) -> tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        hide_parameters=True,
        pool_size=1,
        max_overflow=0,
        pool_timeout=2,
        connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
    )
    return engine, sessionmaker(engine, expire_on_commit=False)
