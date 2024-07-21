from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.dao.base import BaseDAO
from bot_car_number.db.models import Registration


class RegDAO(BaseDAO[Registration]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Registration, session)

    async def get_registrations_count(self, tg_id: int) -> int:
        """Увеличить и вернуть счетчик регистраций пользователя."""
        query = (
            update(Registration)
            .filter_by(tg_id=tg_id)
            .values(count=Registration.count + 1)
        ).returning(Registration.count)
        count = await self.session.execute(query)
        await self.session.commit()
        return count.scalar()
