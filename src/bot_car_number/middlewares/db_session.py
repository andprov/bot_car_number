from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot_car_number.dao.auto import AutoDAO
from bot_car_number.dao.registration import RegDAO
from bot_car_number.dao.stats import StatsDAO
from bot_car_number.dao.user import DatabaseUserGateway
from bot_car_number.db.models import Auto, Registration, Stats, User


class SessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["user_dao"] = DatabaseUserGateway(User, session)
            data["auto_dao"] = AutoDAO(Auto, session)
            data["stats_dao"] = StatsDAO(Stats, session)
            data["registration_dao"] = RegDAO(Registration, session)
            return await handler(event, data)
