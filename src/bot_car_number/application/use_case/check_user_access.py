from bot_car_number.application.gateways.user import UserGateway


class CheckUserAccess:
    def __init__(self, gateway: UserGateway) -> None:
        self.gateway = gateway

    async def __call__(self, tg_id: int) -> bool:
        user = await self.gateway.get_user_by_telegram_id(tg_id=tg_id)
        if not user:
            return True
        return user.active
