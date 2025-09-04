import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class PrivateCheckMiddleware(BaseMiddleware):
    def __init__(self, group: str) -> None:
        self.group = group

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        status = ["creator", "administrator", "member"]
        tg_id = data["event_from_user"].id
        member = await event.bot.get_chat_member(
            chat_id=self.group,
            user_id=tg_id,
        )
        if data["event_chat"].type == "private" and member.status in status:
            return await handler(event, data)

        logger.warning(f"Group access denied for user | [tg_id: {tg_id}]")
