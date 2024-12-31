import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.application.gateways.user_gateway import UserGateway
from bot_car_number.db.models import User as UserDBModel
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
        user_id = result.scalar_one()
        logger.info("add_user - %s", user_id)

    async def get_user(self, user_id: int) -> User | None:
        stmt = select(self.model).filter_by(id=user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.info("get_user - %s", user)
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
        logger.info("get_user_by_telegram_id - %s", user)
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
        logger.info("ban_user - %s", tg_id)

    async def delete_user(self, tg_id: int) -> None:
        stmt = delete(self.model).filter_by(tg_id=tg_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info("delete_user - %s", tg_id)
