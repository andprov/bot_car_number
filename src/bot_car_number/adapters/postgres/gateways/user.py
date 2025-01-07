import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.adapters.postgres.tables import User as UserDBModel
from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.entities.user import User

logger = logging.getLogger(__name__)


class DatabaseUserGateway(UserGateway):
    def __init__(self, session: AsyncSession):
        self.model = UserDBModel
        self.session = session

    async def add_user(self, user: User) -> None:
        stmt = (
            insert(self.model)
            .values(
                tg_id=user.tg_id,
                first_name=user.first_name,
                phone=user.phone,
                banned=user.banned,
            )
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        db_obj = result.scalar_one()
        logger.info(f"add_user - [user.id: {db_obj}]")

    async def get_user(self, user_id: int) -> User | None:
        stmt = select(self.model).filter_by(id=user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.info(f"get_user - [user: {user}]")
        if user:
            return User(
                id=user.id,
                tg_id=user.tg_id,
                first_name=user.first_name,
                phone=user.phone,
                banned=user.banned,
            )

    async def get_user_by_telegram_id(self, tg_id: int) -> User | None:
        stmt = select(self.model).filter_by(tg_id=tg_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.info(f"get_user_by_telegram_id - [user: {user}]")
        if user:
            return User(
                id=user.id,
                tg_id=user.tg_id,
                first_name=user.first_name,
                phone=user.phone,
                banned=user.banned,
            )

    async def ban_user(self, tg_id: int) -> None:
        stmt = update(self.model).filter_by(tg_id=tg_id).values(banned=True)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"ban_user - [tg_id: {tg_id}]")

    async def delete_user(self, tg_id: int) -> None:
        stmt = delete(self.model).filter_by(tg_id=tg_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"delete_user - [tg_id: {tg_id}]")
