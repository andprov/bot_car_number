from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot_car_number.dao.auto import AutoDAO
from bot_car_number.dao.registration import RegDAO
from bot_car_number.dao.stats import StatsDAO
from bot_car_number.dao.user import UserDAO


class DbMiddleware(BaseMiddleware):
    def __init__(
        self,
        session_pool: async_sessionmaker,
    ):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["user_dao"] = UserDAO(session)
            data["auto_dao"] = AutoDAO(session)
            data["stats_dao"] = StatsDAO(session)
            data["registration_dao"] = RegDAO(session)
            return await handler(event, data)
