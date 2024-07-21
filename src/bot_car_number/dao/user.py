from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot_car_number.dao.base import BaseDAO
from bot_car_number.db.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def find_user_with_autos(self, **data) -> User | None:
        """Получить пользователя и его автомобили."""
        query = (
            select(User).options(selectinload(User.autos)).filter_by(**data)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def set_user_banned_true(self, **data) -> None:
        """Обновить значение поля banned на True."""
        query = update(User).filter_by(**data).values(banned=True)
        await self.session.execute(query)
        await self.session.commit()
