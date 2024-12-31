from bot_car_number.config import SEARCH_COUNT_LIMIT
from bot_car_number.dao.stats import DatabaseStatsGateway
from bot_car_number.entities.stats import Stats


class StatsService:
    @classmethod
    async def add_search_try(
        cls, dao: DatabaseStatsGateway, stats: Stats
    ) -> None:
        await dao.add_search_try(stats)

    @classmethod
    async def check_search_access(
        cls, dao: DatabaseStatsGateway, user_id: int
    ) -> bool:
        day_search_count = await dao.get_search_count(user_id)
        return day_search_count < SEARCH_COUNT_LIMIT
