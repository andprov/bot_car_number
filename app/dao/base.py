from typing import Any

from sqlalchemy import delete, insert, select


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, session, **data) -> Any | None:
        """Получить одну запись из базы или None."""
        query = select(cls.model).filter_by(**data)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def add(cls, session, **data) -> None:
        """Добавить запись в базу."""
        query = insert(cls.model).values(**data)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def delete(cls, session, **data) -> None:
        """Удалить запись из базы."""
        query = delete(cls.model).filter_by(**data)
        await session.execute(query)
        await session.commit()
