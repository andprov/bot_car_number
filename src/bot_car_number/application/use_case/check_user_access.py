from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.domain.exceptions import UserNotFoundError


class CheckUserAccess:
    def __init__(self, gateway: UserGateway):
        self.gateway = gateway

    async def __call__(self, tg_id: int) -> bool:
        user = await self.gateway.get_user_by_telegram_id(tg_id=tg_id)
        if not user:
            raise UserNotFoundError(message="User not found")
        return user.banned
