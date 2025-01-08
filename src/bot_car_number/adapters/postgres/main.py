from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot_car_number.adapters.postgres.config import PostgresConfig


def get_async_sesionmaker(config: PostgresConfig):
    engine = create_async_engine(url=config.url, echo=config.echo)
    return async_sessionmaker(engine, expire_on_commit=False)


# TODO: inject this
async def get_session(sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        yield session
