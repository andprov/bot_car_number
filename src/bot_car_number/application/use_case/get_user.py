import logging

from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.exceptions import UserNotFoundError
from bot_car_number.application.interfaces.user import UserGateway

logger = logging.getLogger(__name__)


class GetUser:
    def __init__(self, user_gateway: UserGateway) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, user_id: int) -> UserDTO:
        user = await self.user_gateway.get_user(user_id)
        if user is None:
            logger.warning(f"[UC] User not found | [user_id: {user_id}]")
            raise UserNotFoundError()

        return user
