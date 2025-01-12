from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.gateways.user import UserGateway


class CreateUser:
    def __init__(self, gateway: UserGateway):
        self.gateway = gateway

    async def __call__(self, user: UserDTO) -> None:
        await self.gateway.add_user(user=user)
