from alembic import context
from infrapulse.config import Settings
from sqlalchemy import create_engine, pool, text


def run_migrations() -> None:
    if context.is_offline_mode():
        raise RuntimeError("Run this migration against a live PostgreSQL database")
    engine = create_engine(
        Settings.load().database_url,
        poolclass=pool.NullPool,
        hide_parameters=True,
        connect_args={"connect_timeout": 5},
    )
    try:
        with engine.begin() as connection:
            connection.execute(text("SET LOCAL lock_timeout = '10s'"))
            connection.execute(text("SELECT pg_advisory_xact_lock(487342601)"))
            context.configure(connection=connection)
            context.run_migrations()
    finally:
        engine.dispose()


run_migrations()
