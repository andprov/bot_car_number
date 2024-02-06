from sqlalchemy import update

from app.dao.base import BaseDAO
from app.db.database import async_session
from app.db.models import Registration


class RegistrationsDAO(BaseDAO):
    model = Registration

    @classmethod
    async def get_registrations_count(cls, tg_id) -> int:
        """Увеличить и вернуть счетчик регистраций пользователя."""
        async with async_session() as session:
            query = (
                update(Registration)
                .filter_by(tg_id=tg_id)
                .values(count=Registration.count + 1)
            ).returning(Registration.count)
            count = await session.execute(query)
            await session.commit()
            return count.scalar()
