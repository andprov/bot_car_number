from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.db.models import Registration


class RegDAO:
    def __init__(
        self, model: type[Registration], session: AsyncSession
    ) -> None:
        self.model = model
        self.session = session

    async def add(self, **data) -> None:
        query = insert(self.model).values(**data)
        await self.session.execute(query)
        await self.session.commit()

    async def find_one_or_none(self, **data) -> Registration | None:
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_registrations_count(self, tg_id: int) -> int:
        query = (
            update(Registration)
            .filter_by(tg_id=tg_id)
            .values(count=Registration.count + 1)
        ).returning(Registration.count)
        count = await self.session.execute(query)
        await self.session.commit()
        return count.scalar()
