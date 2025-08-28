from bot_car_number.application.config import MAX_AUTO_COUNT
from bot_car_number.application.interfaces.auto import AutoGateway


class CheckUserAutosCount:
    def __init__(self, auto_gateway: AutoGateway) -> None:
        self.auto_gateway = auto_gateway

    async def __call__(self, user_id: int) -> bool:
        autos = await self.auto_gateway.get_autos_by_user_id(user_id=user_id)
        return len(autos) < MAX_AUTO_COUNT
