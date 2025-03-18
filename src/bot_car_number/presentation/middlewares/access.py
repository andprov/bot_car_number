import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.use_case.check_user_access import (
    CheckUserAccess,
)
from bot_car_number.di.middleware_inject import (
    aiogram_middleware_inject,
)

logger = logging.getLogger(__name__)


class PrivateMiddleware(BaseMiddleware):
    def __init__(self, group: str) -> None:
        self.group = group

    @aiogram_middleware_inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        check_user_access: FromDishka[CheckUserAccess],
    ) -> Any:
        tg_id = data["event_from_user"].id
        status = ["creator", "administrator", "member"]
        member = await event.bot.get_chat_member(
            chat_id=self.group,
            user_id=tg_id,
        )
        user_active = await check_user_access(tg_id=tg_id)
        if (
            data["event_chat"].type == "private"
            and member.status in status
            and user_active
        ):
            return await handler(event, data)
        logger.warning(f"Attempt to access by an inactive user tg_id={tg_id}")
