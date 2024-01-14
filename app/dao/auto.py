from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.db.models import Auto
from app.db.database import async_session


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
