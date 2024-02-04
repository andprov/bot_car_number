from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.config import GROUP
from app.dao.user import UserDAO


class PrivateMiddleware(BaseMiddleware):
    """Пропускать только участников группы в личных сообщениях."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_id = data["event_from_user"].id
        status = ["creator", "administrator", "member"]
        member = await event.bot.get_chat_member(GROUP, tg_id)
        banned = await self.check_user_banned(tg_id)

        if (
            data["event_chat"].type == "private"
            and member.status in status
            and banned is not True
        ):
            return await handler(event, data)

    async def check_user_banned(self, tg_id: int) -> bool:
        """Вернуть статус блокировки пользователя."""
        user = await UserDAO.find_one_or_none(tg_id=tg_id)
        if user:
            return user.banned
