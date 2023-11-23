from aiogram.types import Contact
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import selectinload

from app.config import DB_URL
from app.db.models import User, Auto

async_engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)


async def get_user_query(tg_id: int) -> User | None:
    """Получить пользователя."""
    async with async_session() as session:
        query = select(User).filter(User.tg_id == tg_id)
        res = await session.execute(query)
        return res.scalar_one_or_none()


async def get_user_and_autos_query(tg_id: int) -> User | None:
    """Получить пользователя и его автомобили."""
    async with async_session() as session:
        query = select(User).filter(User.tg_id == tg_id)
        res = await session.execute(query.options(selectinload(User.autos)))
        return res.scalar_one_or_none()


async def get_auto_query(number: str) -> Auto | None:
    """Получить авто из БД."""
    async with async_session() as session:
        query = select(Auto).filter(Auto.number == number)
        res = await session.execute(query)
        return res.scalar_one_or_none()


async def get_auto_and_owner_query(number: str) -> Auto | None:
    """Получить авто и владельца из ДБ."""
    async with async_session() as session:
        query = select(Auto).filter(Auto.number == number)
        res = await session.execute(query.options(selectinload(Auto.owner)))
        return res.scalar_one_or_none()


async def add_user_query(contact: Contact) -> None:
    """Добавить пользователя в БД."""
    async with async_session() as session:
        session.add(
            User(
                tg_id=contact.user_id,
                first_name=contact.first_name,
                phone=contact.phone_number,
            )
        )
        await session.commit()


async def add_auto_query(**kwargs: dict[str]) -> None:
    """Добавить авто в БД."""
    async with async_session() as session:
        session.add(
            Auto(
                number=kwargs["number"],
                model=kwargs["model"],
                owner_id=kwargs["user_id"],
            )
        )
        await session.commit()


async def delete_query(obj: User | Auto) -> None:
    """Удалить объект из БД."""
    async with async_session() as session:
        await session.delete(obj)
        await session.commit()
