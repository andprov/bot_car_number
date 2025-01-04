import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot_car_number.config import load_config
from bot_car_number.presentation.handlers import auto, menu, search, user
from bot_car_number.presentation.middlewares.access import PrivateMiddleware
from bot_car_number.presentation.middlewares.db_session import (
    SessionMiddleware,
)
from bot_car_number.presentation.misc.ui_commands import set_ui_commands
from bot_car_number.services.auto_service import AutoService
from bot_car_number.services.stats_service import StatsService
from bot_car_number.services.user_service import UserService

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Bot start")

    config = load_config()

    redis = Redis(host=config.redis.host, port=config.redis.port)
    storage = RedisStorage(redis=redis)

    engine = create_async_engine(config.db.ulr, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    dp = Dispatcher(
        storage=storage,
        user_service=UserService,
        auto_service=AutoService,
        stats_service=StatsService,
    )
    dp.update.middleware(SessionMiddleware(sessionmaker))
    dp.update.middleware(PrivateMiddleware(config.bot.group))
    dp.include_routers(menu.router, user.router, auto.router, search.router)

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await set_ui_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stop")
