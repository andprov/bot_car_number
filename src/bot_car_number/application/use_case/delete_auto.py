from bot_car_number.application.gateways.auto import AutoGateway


class DeleteAuto:
    def __init__(self, auto_gateway: AutoGateway) -> None:
        self.auto_gateway = auto_gateway

    async def __call__(self, id: int) -> None:
        await self.auto_gateway.delete_auto(id=id)
