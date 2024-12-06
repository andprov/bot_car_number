from datetime import timedelta

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.config import TIME_LIMIT
from bot_car_number.db.models import Stats


class StatsDAO:
    def __init__(self, model: type[Stats], session: AsyncSession):
        self.model = model
        self.session = session

    async def add(self, **data) -> None:
        query = insert(self.model).values(**data)
        await self.session.execute(query)
        await self.session.commit()

    async def get_day_search_count(self, user_id: int) -> int | None:
        query = select(func.count(Stats.id)).where(
            Stats.user_id == user_id,
            Stats.data >= func.now() - timedelta(hours=TIME_LIMIT),
        )
        result = await self.session.execute(query)
        return result.scalar()
