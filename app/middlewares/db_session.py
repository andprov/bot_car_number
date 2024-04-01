from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.services.auto_service import AutoService
from app.services.user_service import UserService


class DbSessionMiddleware(BaseMiddleware):

    def __init__(
        self,
        session_pool: async_sessionmaker,
        user_service: UserService,
        auto_service: AutoService,
    ):
        super().__init__()
        self.session_pool = session_pool
        self.user_service = user_service
        self.auto_service = auto_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            data["user_service"] = self.user_service
            data["auto_service"] = self.auto_service
            return await handler(event, data)
