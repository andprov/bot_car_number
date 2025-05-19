from bot_car_number.application.gateways.user import UserGateway


class DeleteUser:
    def __init__(self, user_gateway: UserGateway) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, id: int) -> None:
        await self.user_gateway.delete_user(id=id)
