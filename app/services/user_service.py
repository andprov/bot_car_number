from aiogram.types import Contact

from app.config import MAX_REGISTRATIONS_COUNT
from app.dao.registration import RegistrationsDAO
from app.dao.user import UserDAO
from app.db.models import User
from db.database import async_session


class UserService:
    """Сервис для работы с пользователями."""

    @classmethod
    async def check_user(cls, tg_id: int) -> bool:
        """Проверить наличие пользователя в базе."""
        async with async_session() as session:
            if await UserDAO.find_one_or_none(session, tg_id=tg_id):
                return True
            return False

    @classmethod
    async def add_user(cls, contact: Contact) -> None:
        """Добавить пользователя в базу."""
        async with async_session() as session:
            await UserDAO.add(
                session,
                tg_id=contact.user_id,
                first_name=contact.first_name,
                phone=contact.phone_number,
            )

    @classmethod
    async def get_user_with_auto(cls, tg_id: int) -> User | None:
        """Вернуть пользователя и его автомобили."""
        async with async_session() as session:
            return await UserDAO.find_user_with_autos(session, tg_id=tg_id)

    @classmethod
    async def delete_user(cls, tg_id: int) -> None:
        """Удалить пользователя из базы."""
        async with async_session() as session:
            await UserDAO.delete(session, tg_id=tg_id)

    @classmethod
    async def check_registration_limit(cls, tg_id: int) -> bool:
        """Добавить запись о регистрации пользователя или увеличить счетчик
        если регистрация уже была.
        """
        async with async_session() as session:
            if not await RegistrationsDAO.find_one_or_none(
                session, tg_id=tg_id
            ):
                await RegistrationsDAO.add(session, tg_id=tg_id)
                return False
            count = await RegistrationsDAO.get_registrations_count(
                session, tg_id=tg_id
            )
        if count > MAX_REGISTRATIONS_COUNT:
            return True
        return False

    @classmethod
    async def block_user(cls, tg_id: int) -> None:
        """Заблокировать пользователя."""
        async with async_session() as session:
            await UserDAO.set_user_banned_true(session, tg_id=tg_id)

    @classmethod
    async def get_user_banned(cls, tg_id: int) -> bool | None:
        """Вернуть статус блокировки пользователя."""
        async with async_session() as session:
            user = await UserDAO.find_one_or_none(session, tg_id=tg_id)
        if user:
            return user.banned


user_service: UserService = UserService()
