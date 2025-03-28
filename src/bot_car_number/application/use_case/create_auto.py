from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.gateways.auto import AutoGateway


class CreateAuto:
    def __init__(self, gateway: AutoGateway) -> None:
        self.gateway = gateway

    async def __call__(self, auto: AutoDTO) -> None:
        if not await self.gateway.get_auto_by_number(number=auto.number):
            await self.gateway.add_auto(auto=auto)
