from dataclasses import dataclass, field

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot_car_number.config_loader import get_env_value


@dataclass(frozen=True)
class RedisConfig:
    host: str = field(default="localhost")
    port: int = field(default=6379)


def load_redis_config() -> RedisConfig:
    return RedisConfig(
        host=get_env_value("REDIS_HOST"),
        port=int(get_env_value("REDIS_PORT")),
    )


def get_redis_storage() -> RedisStorage:
    redis_config = load_redis_config()
    redis = Redis(
        host=redis_config.host,
        port=redis_config.port,
    )
    return RedisStorage(redis=redis)
