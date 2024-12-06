from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot_car_number.db.models import Auto


class AutoDAO:
    def __init__(self, model: type[Auto], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def add(self, **data) -> None:
        query = insert(self.model).values(**data)
        await self.session.execute(query)
        await self.session.commit()

    async def find_one_or_none(self, **data) -> Auto | None:
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_auto_with_owner(self, **data) -> Auto | None:
        query = (
            select(Auto).options(selectinload(Auto.owner)).filter_by(**data)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, **data) -> None:
        query = delete(self.model).filter_by(**data)
        await self.session.execute(query)
        await self.session.commit()
