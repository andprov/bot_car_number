from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.config import TIME_LIMIT
from bot_car_number.dao.base import BaseDAO
from bot_car_number.db.models import Stats


class StatsDAO(BaseDAO[Stats]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Stats, session)

    async def get_day_search_count(self, user_id: int) -> int:
        """Вернуть количество записей в пределах лимита времени."""
        query = select(func.count(Stats.id)).where(
            Stats.user_id == user_id,
            Stats.data >= func.now() - timedelta(hours=TIME_LIMIT),
        )
        result = await self.session.execute(query)
        return result.scalar()
