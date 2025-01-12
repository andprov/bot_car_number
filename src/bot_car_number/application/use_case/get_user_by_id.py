from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.gateways.user import UserGateway


class GetUserById:
    def __init__(self, gateway: UserGateway):
        self.gateway = gateway

    async def __call__(self, user_id: int) -> UserDTO | None:
        return await self.gateway.get_user(user_id=user_id)

