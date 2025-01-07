from dataclasses import dataclass

from bot_car_number.config_loader import get_env_value


@dataclass(frozen=True)
class BotConfig:
    token: str
    group: str


def load_bot_config():
    return BotConfig(
        token=get_env_value("BOT_TOKEN"),
        group=get_env_value("GROUP_ID"),
    )
