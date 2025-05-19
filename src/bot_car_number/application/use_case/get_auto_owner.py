import logging

from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.exceptions import (
    AutoNotFoundError,
    UserNotFoundError,
)
from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.value_objects.auto_number import AutoNumber

logger = logging.getLogger(__name__)


class GetAutoOwner:
    def __init__(
        self,
        user_gateway: UserGateway,
        auto_gateway: AutoGateway,
    ) -> None:
        self.user_gateway = user_gateway
        self.auto_gateway = auto_gateway

    async def __call__(self, number: str) -> UserDTO:
        auto_number = AutoNumber(value=number)
        auto = await self.auto_gateway.get_auto_by_number(
            number=auto_number.value
        )
        if auto is None:
            logger.warning(f"[UC] Auto does not exist | [{auto_number.value}]")
            raise AutoNotFoundError()

        owner = await self.user_gateway.get_user(id=auto.user_id)
        if owner is None:
            logger.error(f"[UC] User does not exist | [{auto_number.value}]")
            raise UserNotFoundError()

        return owner
