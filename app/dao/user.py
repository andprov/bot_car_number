from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.db.database import async_session
from app.db.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all_user_autos(cls, **data):
        """Получить пользователя и его автомобили."""
        async with async_session() as session:
            query = (
                select(User)
                .options(selectinload(User.autos))
                .filter_by(**data)
            )

            res = await session.execute(query)
            return res.scalar_one_or_none()
