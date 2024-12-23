from aiogram.types import Contact

from bot_car_number.config import MAX_REGISTRATIONS_COUNT
from bot_car_number.dao.registration import RegDAO
from bot_car_number.dao.user import DatabaseUserGateway
from bot_car_number.entities.user import User


class UserService:
    """Сервис для работы с пользователями."""

    @classmethod
    async def check_user_exists(
        cls, dao: DatabaseUserGateway, tg_id: int
    ) -> bool:
        """Проверить наличие пользователя в базе."""
        user = await dao.get_user_by_telegram_id(tg_id=tg_id)
        if user:
            return True
        return False

    @classmethod
    async def add_user(
        cls, dao: DatabaseUserGateway, contact: Contact
    ) -> None:
        """Добавить пользователя в базу."""
        user = User(
            tg_id=contact.user_id,
            first_name=contact.first_name,
            phone=contact.phone_number,
            banned=False,
        )
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
        """..."""
        return await dao.get_user_by_telegram_id(tg_id=tg_id)

    @classmethod
    async def delete_user(cls, dao: DatabaseUserGateway, tg_id: int) -> None:
        """Удалить пользователя из базы."""
        await dao.delete_user(tg_id=tg_id)

    @classmethod
    async def check_registration_limit(cls, dao: RegDAO, tg_id: int) -> bool:
        """Добавить запись о регистрации пользователя или увеличить счетчик
        если регистрация уже была.
        """
        if not await dao.find_one_or_none(tg_id=tg_id):
            await dao.add(tg_id=tg_id)
            return False
        count = await dao.get_registrations_count(tg_id=tg_id)
        if count and count > MAX_REGISTRATIONS_COUNT:
            return True
        return False

    @classmethod
    async def block_user(cls, dao: DatabaseUserGateway, tg_id: int) -> None:
        """Заблокировать пользователя."""
        await dao.ban_user(tg_id=tg_id)

    @classmethod
    async def get_user_banned(
        cls, dao: DatabaseUserGateway, tg_id: int
    ) -> bool:
        """Вернуть статус блокировки пользователя."""
        user = await dao.get_user_by_telegram_id(tg_id=tg_id)
        if user:
            return user.banned
        return False
