from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.use_case.get_user_by_telegram_id import (
    GetUserByTelegramId,
)
from bot_car_number.di.middleware_inject import aiogram_middleware_inject


class UserMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
    ) -> Any:
        if "user" not in data:
            tg_id = data["event_from_user"].id
            data["user"] = await get_user_by_telegram_id(tg_id=tg_id)

        return await handler(event, data)
