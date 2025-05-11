from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.gateways.auto import AutoGateway


class AddAuto:
    def __init__(self, auto_gateway: AutoGateway) -> None:
        self.auto_gateway = auto_gateway

    async def __call__(self, auto: AutoDTO) -> None:
        if not await self.auto_gateway.get_auto_by_number(number=auto.number):
            await self.auto_gateway.add_auto(auto=auto)
