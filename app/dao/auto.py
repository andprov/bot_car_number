from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.db.models import Auto


class AutoDAO(BaseDAO):
    model = Auto

    @classmethod
    async def find_auto_with_owner(cls, session, **data) -> Auto | None:
        """Получить автомобиль и владельца."""
        query = (
            select(Auto).options(selectinload(Auto.owner)).filter_by(**data)
        )
        res = await session.execute(query)
        return res.scalar_one_or_none()
