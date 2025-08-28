import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.adapters.postgres.tables import User as UserDBModel
from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.interfaces.user import UserGateway

logger = logging.getLogger(__name__)


class DatabaseUserGateway(UserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.model = UserDBModel
        self.session = session

    async def add_user(self, user: UserDTO) -> None:
        stmt = (
            insert(self.model)
            .values(
                tg_id=user.tg_id,
                first_name=user.first_name,
                phone=user.phone,
                active=user.active,
            )
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        db_obj = result.scalar_one()
        logger.info(f"[DB] Add user | [user.id: {db_obj}]")

    async def get_user(self, id: int) -> UserDTO | None:
        stmt = select(self.model).filter_by(id=id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.info(f"[DB] Get user | [user: {user}]")
        if user:
            return UserDTO(
                id=user.id,
                tg_id=user.tg_id,
                first_name=user.first_name,
                phone=user.phone,
                active=user.active,
            )

    async def get_user_by_telegram_id(self, tg_id: int) -> UserDTO | None:
        stmt = select(self.model).filter_by(tg_id=tg_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.info(f"[DB] Get user by telegram id | [user: {user}]")
        if user:
            return UserDTO(
                id=user.id,
                tg_id=user.tg_id,
                first_name=user.first_name,
                phone=user.phone,
                active=user.active,
            )

    async def block_user(self, tg_id: int) -> None:
        stmt = update(self.model).filter_by(tg_id=tg_id).values(active=False)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"[DB] Ban user | [tg_id: {tg_id}]")

    async def delete_user(self, id: int) -> None:
        stmt = delete(self.model).filter_by(id=id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"[DB] Delete user | [id: {id}]")
