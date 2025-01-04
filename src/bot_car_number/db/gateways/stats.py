import logging
from datetime import timedelta

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.application.gateways.stats_gateway import StatsGateway
from bot_car_number.config import TIME_LIMIT
from bot_car_number.db.models import Stats as StatsDNModel
from bot_car_number.entities.stats import StatsData

logger = logging.getLogger(__name__)


class DatabaseStatsGateway(StatsGateway):
    def __init__(self, session: AsyncSession):
        self.model = StatsDNModel
        self.session = session

    async def add_search_try(self, stats: StatsData) -> None:
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
        return result.scalar()
