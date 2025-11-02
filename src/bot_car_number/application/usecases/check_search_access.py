from bot_car_number.application.config import SEARCH_ATTEMPT_COUNT_LIMIT
from bot_car_number.application.interfaces.search import SearchAttemptGateway


class CheckSearchAccess:
    def __init__(self, search_attempt_gateway: SearchAttemptGateway) -> None:
        self.search_attempt_gateway = search_attempt_gateway

    async def __call__(self, tg_id: int) -> bool:
        search_attempt_count = (
            await self.search_attempt_gateway.get_search_attempt_count(
                tg_id=tg_id
            )
        )
        return search_attempt_count < SEARCH_ATTEMPT_COUNT_LIMIT
