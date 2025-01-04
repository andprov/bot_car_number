from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot_car_number.dao.auto import DatabaseAutoGateway
from bot_car_number.dao.registration import DatabaseRegistrationGateway
from bot_car_number.dao.stats import DatabaseStatsGateway
from bot_car_number.dao.user import DatabaseUserGateway


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
            data["user_dao"] = DatabaseUserGateway(session)
            data["auto_dao"] = DatabaseAutoGateway(session)
            data["stats_dao"] = DatabaseStatsGateway(session)
            data["registration_dao"] = DatabaseRegistrationGateway(session)
            return await handler(event, data)
