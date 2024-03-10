from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.db.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_user_with_autos(cls, session, **data) -> User | None:
        """Получить пользователя и его автомобили."""
        query = (
            select(User).options(selectinload(User.autos)).filter_by(**data)
        )
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def set_user_banned_true(cls, session, **data) -> None:
        """Обновить значение banned пользователя на True."""
        query = update(User).filter_by(**data).values(banned=True)
        await session.execute(query)
        await session.commit()
