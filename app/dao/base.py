from sqlalchemy import select, insert, delete

from app.db.database import async_session


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
