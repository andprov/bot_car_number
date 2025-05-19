from bot_car_number.application.gateways.user import UserGateway


class BlockUser:
    def __init__(self, user_gateway: UserGateway) -> None:
        self.user_gateway = user_gateway

    async def __call__(self, tg_id: int) -> None:
        await self.user_gateway.block_user(tg_id=tg_id)
