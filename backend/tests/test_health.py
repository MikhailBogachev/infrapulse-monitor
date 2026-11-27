import asyncio
import subprocess
import sys

import pytest
from httpx import ASGITransport, AsyncClient
from infrapulse.api import create_app
from infrapulse.config import Settings
from pydantic import SecretStr


def test_liveness_is_independent_of_dependencies() -> None:
    settings = Settings(
        db_host="127.0.0.1:1",
        redis_host="127.0.0.1",
        db_password=SecretStr("synthetic-db"),
        redis_password=SecretStr("synthetic-cache"),
        readiness_timeout=0.3,
    )
    app = create_app(settings)

    async def check() -> None:
        async with (
            app.router.lifespan_context(app),
            AsyncClient(transport=ASGITransport(app=app), base_url="http://fixture") as client,
        ):
            assert (await client.get("/health/live")).json() == {"status": "live"}
            response = await client.get("/health/ready")
            assert response.status_code == 503
            assert response.json() == {"status": "not_ready"}
            assert "synthetic" not in response.text

    asyncio.run(check())


def test_configuration_errors_hide_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INFRAPULSE_DB_PASSWORD", "synthetic-do-not-log")
    monkeypatch.setenv("INFRAPULSE_READINESS_TIMEOUT", "synthetic-do-not-log")
    with pytest.raises(RuntimeError, match="^Invalid InfraPulse service configuration$"):
        Settings.load()


def test_foreign_log_message_and_exception_are_filtered() -> None:
    check = """
import logging
from infrapulse.logging import configure_logging
configure_logging("INFO")
try:
    raise RuntimeError("synthetic-exception-marker")
except RuntimeError:
    logging.getLogger("foreign").exception("synthetic-log-marker")
"""
    result = subprocess.run(
        [sys.executable, "-c", check], capture_output=True, text=True, check=True, timeout=5
    )
    assert '"event": "runtime_event"' in result.stdout
    assert "synthetic" not in result.stdout + result.stderr
