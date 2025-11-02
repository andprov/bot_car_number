import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.usecases.get_user_by_telegram_id import (
    GetUserByTelegramId,
)
from bot_car_number.di.middleware_inject import aiogram_middleware_inject

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
    ) -> Any:
        tg_id = data["event_from_user"].id
        user = await get_user_by_telegram_id(tg_id=tg_id)
        data["user"] = user
        if user is None or user.active:
            return await handler(event, data)

        logger.warning(
            f"[bot] Attempt to access by an block user | [tg_id: {tg_id}]"
        )
