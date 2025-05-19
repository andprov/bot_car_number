import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.use_case.check_user_access import (
    CheckUserAccess,
)
from bot_car_number.di.middleware_inject import aiogram_middleware_inject

logger = logging.getLogger(__name__)


class UserAccessMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        check_user_access: FromDishka[CheckUserAccess],
    ) -> Any:
        tg_id = data["event_from_user"].id
        if await check_user_access(tg_id=tg_id):
            return await handler(event, data)

        logger.warning(f"Attempt to access by an block user tg_id={tg_id}")
