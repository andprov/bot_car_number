from bot_car_number.application.gateways.user import UserGateway


class DeleteUser:
    def __init__(self, gateway: UserGateway):
        self.gateway = gateway

    async def __call__(self, tg_id: int) -> None:
        await self.gateway.delete_user(tg_id=tg_id)
