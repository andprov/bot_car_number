from dataclasses import dataclass, field

from bot_car_number.config_loader import get_env_value


@dataclass(frozen=True)
class RedisConfig:
    host: str = field(default="localhost")
    port: int = field(default=6379)


def load_redis_config():
    return RedisConfig(
        host=get_env_value("REDIS_HOST"),
        port=get_env_value("REDIS_PORT"),
    )
