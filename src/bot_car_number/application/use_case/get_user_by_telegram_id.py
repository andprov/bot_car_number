from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.interfaces.user import UserGateway


class GetUserByTelegramId:
    def __init__(self, user_gateway: UserGateway) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, tg_id: int) -> UserDTO | None:
        return await self.user_gateway.get_user_by_telegram_id(tg_id=tg_id)
