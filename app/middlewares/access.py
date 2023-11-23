from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.config import GROUP


class PrivateMiddleware(BaseMiddleware):
    """Пропускать только участников группы в личных сообщениях."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        status = ["creator", "administrator", "member"]
        member = await event.bot.get_chat_member(
            GROUP, data["event_from_user"].id
        )
        if data["event_chat"].type == "private" and member.status in status:
            return await handler(event, data)
