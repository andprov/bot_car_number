from bot_car_number.application.dto.search import SearchAttemptDTO
from bot_car_number.application.gateways.search import SearchAttemptGateway


class AddSearchAttempt:
    def __init__(self, search_attempt_gateway: SearchAttemptGateway) -> None:
        self.search_attempt_gateway = search_attempt_gateway

    async def __call__(self, search_data: SearchAttemptDTO) -> None:
        await self.search_attempt_gateway.add_search_attempt(
            search_data=search_data
        )
