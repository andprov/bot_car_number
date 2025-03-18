from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.gateways.user import UserGateway


class GetUserByTelegramId:
    def __init__(self, gateway: UserGateway) -> None:
        self.gateway = gateway

    async def __call__(self, tg_id: int) -> UserDTO | None:
        return await self.gateway.get_user_by_telegram_id(tg_id=tg_id)
