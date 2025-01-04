import logging

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.application.gateways.auto_gateway import AutoGateway
from bot_car_number.db.models import Auto as AutoDBModel
from bot_car_number.entities.auto import Auto

logger = logging.getLogger(__name__)


class DatabaseAutoGateway(AutoGateway):
    def __init__(self, session: AsyncSession):
        self.model = AutoDBModel
        self.session = session

    async def add_auto(self, auto: Auto) -> None:
        stmt = (
            insert(self.model)
            .values(
                number=auto.number,
                model=auto.model,
                user_id=auto.user_id,
            )
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        auto_id = result.scalar_one()
        logger.info(f"add_auto - [auto.id: {auto_id}]")

    async def get_auto_by_number(self, number: str) -> Auto | None:
        stmt = select(self.model).filter_by(number=number)
        result = await self.session.execute(stmt)
        auto = result.scalar_one_or_none()
        logger.info(f"get_auto_by_number - [auto: {auto}]")
        if auto:
            return Auto(
                id=auto.id,
                number=auto.number,
                model=auto.model,
                user_id=auto.user_id,
            )

    async def get_autos_by_user_id(self, user_id: int) -> list[Auto | None]:
        stmt = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(stmt)
        autos_data = result.scalars().all()
        autos = [
            Auto(
                id=auto.id,
                number=auto.number,
                model=auto.model,
                user_id=auto.user_id,
            )
            for auto in autos_data
        ]
        logger.info(
            f"get_autos_by_user_id - [user.id: {user_id}, "
            f"len_auto_list: {len(autos)}]"
        )
        return autos

    async def delete_auto(self, id: int) -> None:
        stmt = delete(self.model).filter_by(id=id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"delete_auto - [auto.id: {id}]")
