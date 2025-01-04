import logging

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.adapters.db.models import (
    Registration as RegistrationDBModel,
)
from bot_car_number.application.gateways.registration import (
    RegistrationGateway,
)

logger = logging.getLogger(__name__)


class DatabaseRegistrationGateway(RegistrationGateway):
    def __init__(self, session: AsyncSession):
        self.model = RegistrationDBModel
        self.session = session

    async def add_registration(self, tg_id: int) -> None:
        stmt = insert(self.model).values(tg_id=tg_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"add_registration - [tg_id: {tg_id}]")

    async def get_registrations_count(self, tg_id: int) -> int:
        stmt = select(self.model.count).filter_by(tg_id=tg_id)
        result = await self.session.execute(stmt)
        count = result.scalar_one_or_none() or 0
        logger.info(
            f"get_registrations_count - [tg_id: {tg_id}, count: {count}]"
        )
        return count

    async def increase_registrations_count(self, tg_id: int) -> None:
        stmt = (
            update(self.model)
            .filter_by(tg_id=tg_id)
            .values(count=self.model.count + 1)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"increase_registrations_count - [tg_id: {tg_id}]")
