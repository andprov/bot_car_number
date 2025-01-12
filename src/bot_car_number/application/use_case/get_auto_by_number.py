from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.gateways.auto import AutoGateway


class GetAutoByNumber:
    def __init__(self, gateway: AutoGateway):
        self.gateway = gateway

    async def __call__(self, number: str) -> AutoDTO | None:
        return await self.gateway.get_auto_by_number(number=number)
