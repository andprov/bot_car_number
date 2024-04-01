from aiogram.types import Contact

from app.config import MAX_REGISTRATIONS_COUNT
from app.dao.registration import RegDAO
from app.dao.user import UserDAO
from app.db.models import User


class UserService:
    """Сервис для работы с пользователями."""

    @classmethod
    async def check_user(cls, dao: UserDAO, tg_id: int) -> bool:
        """Проверить наличие пользователя в базе."""
        if await dao.find_one_or_none(tg_id=tg_id):
            return True
        return False

    @classmethod
    async def add_user(cls, dao: UserDAO, contact: Contact) -> None:
        """Добавить пользователя в базу."""
        await dao.add(
            tg_id=contact.user_id,
            first_name=contact.first_name,
            phone=contact.phone_number,
        )

    @classmethod
    async def get_user_with_auto(cls, dao: UserDAO, tg_id: int) -> User | None:
        """Вернуть пользователя и его автомобили."""
        return await dao.find_user_with_autos(tg_id=tg_id)

    @classmethod
    async def delete_user(cls, dao: UserDAO, tg_id: int) -> None:
        """Удалить пользователя из базы."""
        await dao.delete(tg_id=tg_id)

    @classmethod
    async def check_registration_limit(cls, dao: RegDAO, tg_id: int) -> bool:
        """Добавить запись о регистрации пользователя или увеличить счетчик
        если регистрация уже была.
        """
        if not await dao.find_one_or_none(tg_id=tg_id):
            await dao.add(tg_id=tg_id)
            return False
        count = await dao.get_registrations_count(tg_id=tg_id)
        if count > MAX_REGISTRATIONS_COUNT:
            return True
        return False

    @classmethod
    async def block_user(cls, dao: UserDAO, tg_id: int) -> None:
        """Заблокировать пользователя."""
        await dao.set_user_banned_true(tg_id=tg_id)

    @classmethod
    async def get_user_banned(cls, dao: UserDAO, tg_id: int) -> bool | None:
        """Вернуть статус блокировки пользователя."""
        user = await dao.find_one_or_none(tg_id=tg_id)
        if user:
            return user.banned
