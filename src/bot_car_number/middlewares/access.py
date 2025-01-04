from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot_car_number.adapters.db.gateways.user import DatabaseUserGateway
from bot_car_number.services.user_service import UserService


class PrivateMiddleware(BaseMiddleware):
    def __init__(self, group: str):
        self.group = group

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_id = data["event_from_user"].id
        user_dao: DatabaseUserGateway = data["user_dao"]
        user_service: UserService = data["user_service"]
        status = ["creator", "administrator", "member"]
        member = await event.bot.get_chat_member(self.group, tg_id)
        banned = await user_service.get_user_banned(user_dao, tg_id)

        if (
            data["event_chat"].type == "private"
            and member.status in status
            and not banned
        ):
            return await handler(event, data)
