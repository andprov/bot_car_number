from dataclasses import dataclass, field

from bot_car_number.config_loader import get_env_value


@dataclass(frozen=True)
class PostgresConfig:
    user: str = field(default="postgres")
    password: str = field(default="postgres")
    host: str = field(default="localhost")
    port: int = field(default=5432)
    database: str = field(default="bot_car_number")
    echo: bool = field(default=False)

    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


def load_postgres_config() -> PostgresConfig:
    return PostgresConfig(
        user=get_env_value("POSTGRES_USER") or None,
        password=get_env_value("POSTGRES_PASSWORD") or None,
        host=get_env_value("DB_HOST") or None,
        port=int(get_env_value("DB_PORT")) or None,
        database=get_env_value("POSTGRES_DB") or None,
        echo=get_env_value("ECHO") == "True",
    )
