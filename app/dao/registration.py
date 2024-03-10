from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.db.models import Registration


class RegistrationsDAO(BaseDAO):
    model = Registration

    @classmethod
    async def get_registrations_count(
        cls, session: AsyncSession, tg_id: int
    ) -> int:
        """Увеличить и вернуть счетчик регистраций пользователя."""
        query = (
            update(Registration)
            .filter_by(tg_id=tg_id)
            .values(count=Registration.count + 1)
        ).returning(Registration.count)
        count = await session.execute(query)
        await session.commit()
        return count.scalar()
