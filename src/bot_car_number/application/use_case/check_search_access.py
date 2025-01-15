from bot_car_number.application.gateways.stats import StatsGateway
from bot_car_number.config_loader import SEARCH_COUNT_LIMIT


class CheckSearchAccess:
    def __init__(self, gateway: StatsGateway) -> None:
        self.gateway = gateway

    async def __call__(self, user_id: int) -> bool:
        search_count = await self.gateway.get_search_count(user_id=user_id)
        return search_count < SEARCH_COUNT_LIMIT
