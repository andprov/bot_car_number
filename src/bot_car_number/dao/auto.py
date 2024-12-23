from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.application.gateways.auto_gateway import AutoGateway
from bot_car_number.db.models import Auto as AutoDBModel
from bot_car_number.entities.auto import Auto


class DatabaseAutoGateway(AutoGateway):
    # def __init__(self, model: type[AutoDBModel], session: AsyncSession):
    def __init__(self, session: AsyncSession):
        self.model = AutoDBModel
        self.session = session

    async def add_auto(self, auto: Auto) -> None:
        query = insert(self.model).values(
            number=auto.number,
            model=auto.model,
            user_id=auto.user_id,
        )
        await self.session.execute(query)
        await self.session.commit()


    async def get_auto_by_number(self, number: str) -> Auto | None:
        query = select(self.model).filter_by(number=number)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_autos_by_user_id(self, user_id: int) -> list[Auto | None]:
        query = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(query)
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
        return autos

    async def delete_auto(self, id: int) -> None:
        query = delete(self.model).filter_by(id=id)
        await self.session.execute(query)
        await self.session.commit()
