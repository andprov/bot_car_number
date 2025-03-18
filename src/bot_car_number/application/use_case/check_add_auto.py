from bot_car_number.application.config import MAX_AUTO_COUNT
from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.domain.exceptions import UserNotFoundError
from bot_car_number.presentation.misc.msg import AUTO_MAX_COUNT_MSG


class CheckUserAutosCount:
    def __init__(
        self,
        user_gateway: UserGateway,
        auto_gateway: AutoGateway,
    ) -> None:
        self.user_gateway = user_gateway
        self.auto_gateway = auto_gateway

    async def __call__(self, tg_id: int) -> tuple[UserDTO | None, None | str]:
        user = await self.user_gateway.get_user_by_telegram_id(tg_id=tg_id)
        if not user:
            raise UserNotFoundError(message="User not found")

        autos = await self.auto_gateway.get_autos_by_user_id(user_id=user.id)
        if len(autos) >= MAX_AUTO_COUNT:
            return None, AUTO_MAX_COUNT_MSG

        return user, None
