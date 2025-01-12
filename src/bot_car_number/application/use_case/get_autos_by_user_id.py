from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.gateways.auto import AutoGateway


class GetAutosByUserId:
    def __init__(self, gateway: AutoGateway):
        self.gateway = gateway

    async def __call__(self, user_id: int) -> list[AutoDTO | None]:
        return await self.gateway.get_autos_by_user_id(user_id=user_id)
