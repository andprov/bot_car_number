import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka.integrations.aiogram import setup_dishka

from bot_car_number.adapters.postgres.config import load_postgres_config
from bot_car_number.adapters.redis.config import get_redis_storage
from bot_car_number.di.providers import setup_async_container
from bot_car_number.presentation.config import load_bot_config
from bot_car_number.presentation.handlers.auto import router as auto_router
from bot_car_number.presentation.handlers.block_auto import (
    router as block_router,
)
from bot_car_number.presentation.handlers.menu import router as menu_router
from bot_car_number.presentation.handlers.user import router as user_router
from bot_car_number.presentation.middlewares.private_check import (
    PrivateCheckMiddleware,
)
from bot_car_number.presentation.middlewares.user import UserMiddleware
from bot_car_number.presentation.misc.ui_commands import set_ui_commands

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-19s - %(levelname)-8s - %(message)-100s - %(name)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("[bot] Bot start")

    bot_config = load_bot_config()

    storage = get_redis_storage()

    dp = Dispatcher(storage=storage)
    dp.update.middleware(PrivateCheckMiddleware(bot_config.group))
    dp.update.middleware(UserMiddleware())
    dp.include_routers(
        menu_router,
        user_router,
        auto_router,
        block_router,
    )

    bot = Bot(
        token=bot_config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    db_config = load_postgres_config()
    container = setup_async_container(db_config)
    setup_dishka(container=container, router=dp, auto_inject=True)

    await set_ui_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("[bot] Bot stop")
