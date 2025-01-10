from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot_car_number.adapters.postgres.config import PostgresConfig


def get_async_sessionmaker(config: PostgresConfig) -> async_sessionmaker:
    engine = create_async_engine(url=config.url, echo=config.echo)
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_session(
    session_maker: async_sessionmaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
