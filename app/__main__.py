import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import config
from app.handlers import auto, menu, search, user
from app.middlewares.access import PrivateMiddleware
from app.middlewares.db_session import DbSessionMiddleware
from app.misc.ui_commands import set_ui_commands
from app.services.user_service import user_service


async def main():
    redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    storage = RedisStorage(redis=redis)

    engine = create_async_engine(config.DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    dp = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(sessionmaker))
    dp.update.middleware(PrivateMiddleware(config.GROUP, user_service))
    dp.include_routers(menu.router, user.router, auto.router, search.router)

    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

    await set_ui_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format=config.LOG_FORMAT)
    asyncio.run(main())
