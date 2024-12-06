from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot_car_number.db.models import User


class UserDAO:
    def __init__(self, model: type[User], session: AsyncSession):
        self.model = model
        self.session = session

    async def add(self, **data) -> None:
        query = insert(self.model).values(**data)
        await self.session.execute(query)
        await self.session.commit()

    async def find_one_or_none(self, **data) -> User | None:
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_user_with_autos(self, **data) -> User | None:
        query = (
            select(User).options(selectinload(User.autos)).filter_by(**data)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def set_user_banned_true(self, **data) -> None:
        query = update(User).filter_by(**data).values(banned=True)
        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, **data) -> None:
        query = delete(self.model).filter_by(**data)
        await self.session.execute(query)
        await self.session.commit()
