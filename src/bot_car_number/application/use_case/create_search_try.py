from bot_car_number.application.dto.stats import StatsDTO
from bot_car_number.application.gateways.stats import StatsGateway


class CreateSearchTry:
    def __init__(self, gateway: StatsGateway) -> None:
        self.gateway = gateway

    async def __call__(self, stats: StatsDTO) -> None:
        await self.gateway.add_search_try(stats=stats)
