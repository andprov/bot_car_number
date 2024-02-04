from sqlalchemy import select, update
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

    @classmethod
    async def block_user(cls, tg_id):
        """Заблокировать пользователя."""
        async with async_session() as session:
            await session.execute(
                update(cls.model).filter_by(tg_id=tg_id).values(banned=True)
            )
            await session.commit()
