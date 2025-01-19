import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dishka.integrations.aiogram import setup_dishka
from redis.asyncio import Redis

from bot_car_number.adapters.postgres.config import load_postgres_config
from bot_car_number.adapters.redis.config import load_redis_config
from bot_car_number.di.providers import setup_async_container
from bot_car_number.presentation.config import load_bot_config
from bot_car_number.presentation.handlers import auto, menu, search, user
from bot_car_number.presentation.misc.ui_commands import set_ui_commands
from bot_car_number.services.user_service import UserService

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Bot start")

    #
    redis_config = load_redis_config()
    redis = Redis(
        host=redis_config.host,
        port=redis_config.port,
    )
    storage = RedisStorage(redis=redis)
    #

    dp = Dispatcher(
        storage=storage,
        user_service=UserService,
    )

    bot_config = load_bot_config()
    # TODO: fix
    # dp.update.middleware(PrivateMiddleware(bot_config.group))
    # dp.update.middleware(SessionMiddleware(sessionmaker))
    dp.include_routers(menu.router, user.router, auto.router, search.router)

    bot = Bot(
        token=bot_config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    #
    db_config = load_postgres_config()
    container = setup_async_container(db_config)
    setup_dishka(container=container, router=dp)
    #

    await set_ui_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stop")
