from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.db.models import Auto


class AutoDAO(BaseDAO[Auto]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Auto, session)

    async def find_auto_with_owner(self, **data) -> Auto | None:
        """Получить автомобиль и владельца."""
        query = (
            select(Auto).options(selectinload(Auto.owner)).filter_by(**data)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
