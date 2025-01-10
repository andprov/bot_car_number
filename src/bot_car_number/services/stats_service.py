from bot_car_number.adapters.postgres.gateways.stats import DatabaseStatsGateway
from bot_car_number.application.dto.stats import StatsDTO
from bot_car_number.config_loader import SEARCH_COUNT_LIMIT


class StatsService:
    @classmethod
    async def add_search_try(
        cls, dao: DatabaseStatsGateway, stats: StatsDTO
    ) -> None:
        await dao.add_search_try(stats)

    @classmethod
    async def check_search_access(
        cls, dao: DatabaseStatsGateway, user_id: int
    ) -> bool:
        search_count = await dao.get_search_count(user_id)
        return search_count < SEARCH_COUNT_LIMIT
