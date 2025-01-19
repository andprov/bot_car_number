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
        user=get_env_value("POSTGRES_USER"),
        password=get_env_value("POSTGRES_PASSWORD"),
        host=get_env_value("DB_HOST"),
        port=get_env_value("DB_PORT"),
        database=get_env_value("POSTGRES_DB"),
        echo=get_env_value("ECHO") == "True",
    )
