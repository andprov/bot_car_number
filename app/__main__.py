import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.middlewares.access import PrivateMiddleware
from app.middlewares.database import DbSessionMiddleware
from app.config import BOT_TOKEN, LOG_FORMAT, DB_URL
from app.handlers import user, menu, auto, search
from app.services.ui_commands import set_ui_commands


async def main():
    engine = create_async_engine(DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(PrivateMiddleware())
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_routers(menu.router, user.router, auto.router, search.router)

    await set_ui_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    asyncio.run(main())
