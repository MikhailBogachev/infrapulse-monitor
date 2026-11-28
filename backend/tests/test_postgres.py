import shutil

import pytest
from infrapulse.config import Settings
from infrapulse.database import make_async_sessions, make_sync_sessions
from pydantic import SecretStr
from sqlalchemy import text


@pytest.mark.integration
def test_postgres_sessions() -> None:
    import asyncio

    from testcontainers.postgres import PostgresContainer

    if not shutil.which("docker"):
        pytest.skip("Docker CLI unavailable")
    with PostgresContainer(
        "postgres:17.9-bookworm",
        username="fixture",
        password="synthetic-fixture",
        dbname="infrapulse",
    ).with_bind_ports(5432, ("127.0.0.1", None)) as postgres:
        settings = Settings(
            db_host=f"{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}",
            db_user="fixture",
            db_password=SecretStr("synthetic-fixture"),
        )
        engine, sessions = make_sync_sessions(settings)
        try:
            with sessions.begin() as session:
                session.execute(text("CREATE TABLE transactions (id integer PRIMARY KEY)"))

            async def rollback() -> None:
                async_engine, async_sessions = make_async_sessions(settings)
                try:
                    async with async_sessions() as session:
                        await session.execute(text("INSERT INTO transactions VALUES (1)"))
                        await session.rollback()
                finally:
                    await async_engine.dispose()

            asyncio.run(rollback())
            with sessions() as session:
                assert session.scalar(text("SELECT count(*) FROM transactions")) == 0
        finally:
            engine.dispose()
