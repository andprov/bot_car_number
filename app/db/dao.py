from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload

from app.db.database import async_session
from app.db.models import User, Auto


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **data):
        """Вернуть одну запись из DB или None."""
        async with async_session() as session:
            query = select(cls.model).filter_by(**data)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        """Добавить запись в DB."""
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **data):
        """Удалить запись из DB."""
        async with async_session() as session:
            query = delete(cls.model).filter_by(**data)
            await session.execute(query)
            await session.commit()


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


class AutoDAO(BaseDAO):
    model = Auto

    @classmethod
    async def find_auto_with_owner(cls, **data):
        """Получить автомобиль и владельца."""
        async with async_session() as session:
            query = (
                select(Auto)
                .options(selectinload(Auto.owner))
                .filter_by(**data)
            )

            res = await session.execute(query)
            return res.scalar_one_or_none()
