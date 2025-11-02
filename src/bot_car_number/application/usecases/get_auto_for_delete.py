import logging

from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.exceptions import (
    AutoNotFoundError,
    AutoOwnerError,
)
from bot_car_number.application.interfaces.auto import AutoGateway
from bot_car_number.value_objects.auto_number import AutoNumber

logger = logging.getLogger(__name__)


class GetAutoForDelete:
    def __init__(self, auto_gateway: AutoGateway) -> None:
        self.auto_gateway = auto_gateway

    async def __call__(self, number: str, user: UserDTO) -> AutoDTO:
        auto_number = AutoNumber(value=number)
        auto = await self.auto_gateway.get_auto_by_number(
            number=auto_number.value
        )
        if auto is None:
            logger.warning(f"[UC] Auto does not exist | [{auto_number.value}]")
            raise AutoNotFoundError()

        if user.id != auto.user_id:
            logger.warning(
                f"[UC] Access denied. Auto owner is not the current user | "
                f"[user: id={user.id}, auto: id={auto.id}] "
            )
            raise AutoOwnerError()

        return auto
