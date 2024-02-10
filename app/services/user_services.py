from aiogram.types import Contact

from app.config import MAX_REGISTRATIONS_COUNT
from app.dao.registration import RegistrationsDAO
from app.dao.user import UserDAO
from app.db.models import User


class UserService:
    """Сервис для работы с пользователями."""

    @classmethod
    async def check_user(cls, tg_id: int) -> bool:
        """Проверить наличие пользователя в базе."""
        if await UserDAO.find_one_or_none(tg_id=tg_id):
            return True
        return False

    @classmethod
    async def validate_contact(cls, contact: Contact, tg_id: int) -> bool:
        """Проверить, что переданный контакт совпадает с пользователем."""
        if contact.user_id == tg_id:
            return True
        return False

    @classmethod
    async def add_user(cls, contact: Contact) -> None:
        """Добавить пользователя в базу."""
        await UserDAO.add(
            tg_id=contact.user_id,
            first_name=contact.first_name,
            phone=contact.phone_number,
        )

    @classmethod
    async def get_user_with_auto(cls, tg_id: int) -> User | None:
        """Вернуть пользователя и его автомобилями."""
        return await UserDAO.find_user_with_autos(tg_id=tg_id)

    @classmethod
    async def delete_user(cls, tg_id: int) -> None:
        """Удалить пользователя из базы."""
        await UserDAO.delete(tg_id=tg_id)

    @classmethod
    async def check_registration_limit(cls, tg_id: int) -> bool:
        """Добавить запись о регистрации пользователя или увеличить счетчик
        если регистрация уже была.
        """
        if not await RegistrationsDAO.find_one_or_none(tg_id=tg_id):
            await RegistrationsDAO.add(tg_id=tg_id)
            return False
        count = await RegistrationsDAO.get_registrations_count(tg_id=tg_id)
        if count > MAX_REGISTRATIONS_COUNT:
            return True
        return False

    @classmethod
    async def block_user(cls, tg_id: int) -> None:
        """Заблокировать пользователя."""
        await UserDAO.set_user_banned_true(tg_id=tg_id)
