from bot_car_number.application.gateways.auto import AutoGateway


class DeleteAuto:
    def __init__(self, gateway: AutoGateway) -> None:
        self.gateway = gateway

    async def __call__(self, id: int) -> None:
        await self.gateway.delete_auto(id=id)
