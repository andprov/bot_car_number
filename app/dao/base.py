from typing import Generic, Type, TypeVar

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base

Model = TypeVar("Model", Base, Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def find_one_or_none(self, **data) -> Model | None:
        """Получить одну запись из базы или None."""
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, **data) -> None:
        """Добавить запись в базу."""
        query = insert(self.model).values(**data)
        await self.session.execute(query)
        await self.session.commit()

    async def delete(self, **data) -> None:
        """Удалить запись из базы."""
        query = delete(self.model).filter_by(**data)
        await self.session.execute(query)
        await self.session.commit()
