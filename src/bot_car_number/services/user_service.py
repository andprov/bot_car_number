from bot_car_number.adapters.postgres.gateways.registration import (
    DatabaseRegistrationGateway,
)
from bot_car_number.adapters.postgres.gateways.user import DatabaseUserGateway
from bot_car_number.config_loader import MAX_REGISTRATIONS_COUNT
from bot_car_number.entities.user import User


class UserService:
    @classmethod
    async def add_user(cls, dao: DatabaseUserGateway, user: User) -> None:
        await dao.add_user(user)

    @classmethod
    async def get_user(
        cls, dao: DatabaseUserGateway, user_id: int
    ) -> User | None:
        return await dao.get_user(user_id=user_id)

    @classmethod
    async def get_user_by_telegram_id(
        cls, dao: DatabaseUserGateway, tg_id: int
    ) -> User | None:
        return await dao.get_user_by_telegram_id(tg_id=tg_id)

    @classmethod
    async def delete_user(cls, dao: DatabaseUserGateway, tg_id: int) -> None:
        await dao.delete_user(tg_id=tg_id)

    @classmethod
    async def check_registration_limit(
        cls,
        dao: DatabaseRegistrationGateway,
        tg_id: int,
    ) -> bool:
        registration_count = await dao.get_registrations_count(tg_id=tg_id)
        if registration_count > MAX_REGISTRATIONS_COUNT:
            return True
        if registration_count == 0:
            await dao.add_registration(tg_id=tg_id)
            return False
        await dao.increase_registrations_count(tg_id=tg_id)
        return False

    @classmethod
    async def block_user(cls, dao: DatabaseUserGateway, tg_id: int) -> None:
        await dao.ban_user(tg_id=tg_id)

    @classmethod
    async def get_user_banned(
        cls, dao: DatabaseUserGateway, tg_id: int
    ) -> bool:
        user = await dao.get_user_by_telegram_id(tg_id=tg_id)
        if user:
            return user.banned
        return False
