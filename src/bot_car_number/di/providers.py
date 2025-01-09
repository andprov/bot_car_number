from asyncio.log import logger

from dishka import AsyncContainer, Provider, Scope, make_async_container
from dishka.integrations.aiogram import AiogramProvider
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from bot_car_number.adapters.postgres.config import PostgresConfig
from bot_car_number.adapters.postgres.gateways.auto import DatabaseAutoGateway
from bot_car_number.adapters.postgres.gateways.registration import (
    DatabaseRegistrationGateway,
)
from bot_car_number.adapters.postgres.gateways.stats import (
    DatabaseStatsGateway,
)
from bot_car_number.adapters.postgres.gateways.user import DatabaseUserGateway
from bot_car_number.adapters.postgres.main import (
    get_async_engine,
    get_session,
)
from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.application.gateways.registration import (
    RegistrationGateway,
)
from bot_car_number.application.gateways.stats import StatsGateway
from bot_car_number.application.gateways.user import UserGateway


def setup_async_container(postgres_config: PostgresConfig) -> AsyncContainer:
    provider = Provider()
    setup_provider(provider=provider)

    return make_async_container(
        provider,
        AiogramProvider(),
        context={PostgresConfig: postgres_config},
    )


def setup_provider(provider: Provider) -> None:
    provider_config(provider=provider)
    provide_db(provider=provider)
    provide_db_gateways(provider=provider)


def provider_config(provider: Provider) -> None:
    provider.from_context(scope=Scope.APP, provides=PostgresConfig)


def provide_db(provider: Provider) -> None:
    provider.provide(
        source=get_async_engine,
        scope=Scope.APP,
        provides=async_sessionmaker,
    )
    provider.provide(
        source=get_session,
        scope=Scope.REQUEST,
        provides=AsyncSession,
    )


def provide_db_gateways(provider: Provider) -> None:
    logger.info("Registering DatabaseUserGateway...")
    provider.provide(
        source=DatabaseUserGateway,
        scope=Scope.REQUEST,
        provides=UserGateway,
    )
    provider.provide(
        source=DatabaseAutoGateway,
        scope=Scope.REQUEST,
        provides=AutoGateway,
    )
    provider.provide(
        source=DatabaseStatsGateway,
        scope=Scope.REQUEST,
        provides=StatsGateway,
    )
    provider.provide(
        source=DatabaseRegistrationGateway,
        scope=Scope.REQUEST,
        provides=RegistrationGateway,
    )
