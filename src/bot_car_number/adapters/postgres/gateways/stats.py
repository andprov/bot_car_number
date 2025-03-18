import logging
from datetime import timedelta

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.adapters.postgres.tables import Stats as StatsDNModel
from bot_car_number.application.config import TIME_LIMIT
from bot_car_number.application.dto.stats import StatsDTO
from bot_car_number.application.gateways.stats import StatsGateway

logger = logging.getLogger(__name__)


class DatabaseStatsGateway(StatsGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.model = StatsDNModel
        self.session = session

    async def add_search_try(self, stats: StatsDTO) -> None:
        stmt = insert(self.model).values(
            user_id=stats.user_id,
            number=stats.number,
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"add_search_try - [user.id: {stats.user_id}]")

    async def get_search_count(self, user_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(
            self.model.user_id == user_id,
            self.model.date >= func.now() - timedelta(hours=TIME_LIMIT),
        )
        result = await self.session.execute(stmt)
        logger.info(f"get_search_count - [user.id: {user_id}]")
        return result.scalar_one()
