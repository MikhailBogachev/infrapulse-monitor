"""Check that diagnostics redact fixture credentials before writing artifacts."""

from pathlib import Path

from topology_diagnostics import redact


def test_redact_credentials_and_private_key(tmp_path: Path) -> None:
    secret = tmp_path / "infrapulse_broker_password"
    secret.write_text("synthetic/value\n")
    key = tmp_path / "key.pem"
    key.write_text("-----BEGIN PRIVATE KEY-----\nsynthetic-key-body\n-----END PRIVATE KEY-----\n")
    logs = (
        "worker connected to amqp://user:synthetic%2Fvalue@rabbitmq:5672//\n",
        "TLS diagnostic synthetic-key-body\n",
        "password was synthetic/value\n",
        "worker ready\n",
    )
    assert list(redact(logs, tmp_path, key)) == [
        "worker connected to amqp://[redacted]@rabbitmq:5672//\n",
        "TLS diagnostic [redacted]\n",
        "password was [redacted]\n",
        "worker ready\n",
    ]
