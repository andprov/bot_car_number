from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.services.user_service import UserService


class PrivateMiddleware(BaseMiddleware):
    def __init__(self, group: str, user_service: UserService):
        self.user_service = user_service
        self.group = group

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session = data["session"]
        tg_id = data["event_from_user"].id
        status = ["creator", "administrator", "member"]
        member = await event.bot.get_chat_member(self.group, tg_id)
        banned = await self.user_service.get_user_banned(session, tg_id)

        if (
            data["event_chat"].type == "private"
            and member.status in status
            and not banned
        ):
            return await handler(event, data)
