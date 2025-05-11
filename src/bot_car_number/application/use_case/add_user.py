from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.gateways.user import UserGateway


class AddUser:
    def __init__(self, user_gateway: UserGateway) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, user: UserDTO) -> None:
        await self.user_gateway.add_user(user=user)
