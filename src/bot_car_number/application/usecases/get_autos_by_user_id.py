from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.interfaces.auto import AutoGateway


class GetAutosByUserId:
    def __init__(self, auto_gateway: AutoGateway) -> None:
        self.auto_gateway = auto_gateway

    async def __call__(self, user_id: int) -> list[AutoDTO]:
        return await self.auto_gateway.get_autos_by_user_id(user_id=user_id)
