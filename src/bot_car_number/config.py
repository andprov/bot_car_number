import os
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)

MAX_AUTO_COUNT = 10
MAX_AUTO_NAME_LEN = 50
MAX_REGISTRATIONS_COUNT = 5
SEARCH_COUNT_LIMIT = 3
TIME_LIMIT = 3

# DB
DB_TYPE = "DB_TYPE"
DB_CONNECTOR = "DB_CONNECTOR"
DB_HOST = "DB_HOST"
DB_PORT = "DB_PORT"
POSTGRES_DB = "POSTGRES_DB"
POSTGRES_USER = "POSTGRES_USER"
POSTGRES_PASSWORD = "POSTGRES_PASSWORD"

# REDIS
REDIS_HOST = "REDIS_HOST"
REDIS_PORT = "REDIS_PORT"

# BOT
BOT_TOKEN = "BOT_TOKEN"
GROUP_ID = "GROUP_ID"


@dataclass
class DBConfig:
    db_type: str
    connector: str
    host: str
    port: str
    name: str
    user: str
    password: str

    @property
    def ulr(self) -> str:
        return (
            f"{self.db_type}+{self.connector}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


@dataclass
class RedisConfig:
    host: str
    port: str


@dataclass
class BotConfig:
    token: str
    group: str


@dataclass
class Config:
    db: DBConfig
    redis: RedisConfig
    bot: BotConfig


def get_env_value(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is not set")
    return value


def load_config():
    return Config(
        db=DBConfig(
            db_type=get_env_value(DB_TYPE),
            connector=get_env_value(DB_CONNECTOR),
            host=get_env_value(DB_HOST),
            port=get_env_value(DB_PORT),
            name=get_env_value(POSTGRES_DB),
            user=get_env_value(POSTGRES_USER),
            password=get_env_value(POSTGRES_PASSWORD),
        ),
        redis=RedisConfig(
            host=get_env_value(REDIS_HOST),
            port=get_env_value(REDIS_PORT),
        ),
        bot=BotConfig(
            token=get_env_value(BOT_TOKEN),
            group=get_env_value(GROUP_ID),
        ),
    )
