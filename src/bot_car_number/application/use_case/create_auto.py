from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.gateways.auto import AutoGateway


class CreateAuto:
    def __init__(self, gateway: AutoGateway):
        self.gateway = gateway

    async def __call__(self, auto: AutoDTO) -> None:
        await self.gateway.add_auto(auto=auto)
