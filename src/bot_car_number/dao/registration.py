import logging

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.application.gateways.registration_gateway import (
    RegistrationGateway,
)
from bot_car_number.db.models import Registration as RegistrationDBModel

logger = logging.getLogger(__name__)


class DatabaseRegistrationGateway(RegistrationGateway):
    def __init__(self, session: AsyncSession):
        self.model = RegistrationDBModel
        self.session = session

    async def add_registration(self, tg_id: int) -> None:
        stmt = insert(self.model).values(tg_id=tg_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info("add_registration tg_id - %s", tg_id)

    async def find_one_or_none(self, **data):
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_registrations_count(self, tg_id: int) -> int | None:
        query = (
            update(self.model)
            .filter_by(tg_id=tg_id)
            .values(count=self.model.count + 1)
        ).returning(self.model.count)
        count = await self.session.execute(query)
        await self.session.commit()
        return count.scalar()

    async def increase_registrations_count(self, tg_id: int):
        pass
