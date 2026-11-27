from pathlib import Path
from typing import Literal
from urllib.parse import quote

from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="INFRAPULSE_",
        secrets_dir=Path("/run/secrets") if Path("/run/secrets").is_dir() else None,
        hide_input_in_errors=True,
    )

    db_host: str = "postgres"
    db_user: str = "infrapulse_app"
    db_password: SecretStr | None = None
    broker_host: str = "rabbitmq"
    broker_user: str = "infrapulse"
    broker_password: SecretStr | None = None
    redis_host: str = "redis"
    redis_password: SecretStr | None = None
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    readiness_timeout: float = Field(default=2, gt=0, le=10)

    @classmethod
    def load(cls) -> "Settings":
        try:
            return cls()
        except ValidationError:
            raise RuntimeError("Invalid InfraPulse service configuration") from None

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{quote(self.db_user, safe='')}:"
            f"{credential(self.db_password)}@{self.db_host}/infrapulse"
        )

    @property
    def broker_url(self) -> str:
        return (
            f"amqp://{quote(self.broker_user, safe='')}:{credential(self.broker_password)}"
            f"@{self.broker_host}:5672//"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://:{credential(self.redis_password)}@{self.redis_host}:6379/0"


def credential(value: SecretStr | None) -> str:
    if value is None or not value.get_secret_value():
        raise RuntimeError("Required service credential is missing")
    return quote(value.get_secret_value(), safe="")


def contains_live_process(path: Path) -> bool:
    try:
        pid = int(path.read_text().strip())
        stat = Path(f"/proc/{pid}/stat").read_text()
        return stat.rsplit(")", 1)[1].split()[0] != "Z"
    except (OSError, ValueError, IndexError):
        return False
