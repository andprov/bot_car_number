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
    get_async_sessionmaker,
    get_session,
)
from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.application.gateways.registration import (
    RegistrationGateway,
)
from bot_car_number.application.gateways.stats import StatsGateway
from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.application.use_case.add_registration_count import (
    AddRegistrationCount,
)
from bot_car_number.application.use_case.block_user import BlockUser
from bot_car_number.application.use_case.check_search_access import (
    CheckSearchAccess,
)
from bot_car_number.application.use_case.create_auto import CreateAuto
from bot_car_number.application.use_case.create_search_try import (
    CreateSearchTry,
)
from bot_car_number.application.use_case.create_user import CreateUser
from bot_car_number.application.use_case.delete_auto import DeleteAuto
from bot_car_number.application.use_case.delete_user import DeleteUser
from bot_car_number.application.use_case.get_auto_by_number import (
    GetAutoByNumber,
)
from bot_car_number.application.use_case.get_autos_by_user_id import (
    GetAutosByUserId,
)
from bot_car_number.application.use_case.get_user_by_id import GetUserById
from bot_car_number.application.use_case.get_user_by_telegram_id import (
    GetUserByTelegramId,
)


def setup_async_container(postgres_config: PostgresConfig) -> AsyncContainer:
    provider = Provider()
    setup_provider(provider=provider)

    return make_async_container(
        provider,
        AiogramProvider(),
        context={PostgresConfig: postgres_config},
    )


def setup_provider(provider: Provider) -> None:
    provide_config(provider=provider)
    provide_db(provider=provider)
    provide_db_gateways(provider=provider)
    provide_handlers_command(provider=provider)


def provide_config(provider: Provider) -> None:
    provider.from_context(scope=Scope.APP, provides=PostgresConfig)


def provide_db(provider: Provider) -> None:
    provider.provide(
        source=get_async_sessionmaker,
        scope=Scope.APP,
        provides=async_sessionmaker,
    )
    provider.provide(
        source=get_session,
        scope=Scope.REQUEST,
        provides=AsyncSession,
    )


def provide_db_gateways(provider: Provider) -> None:
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


def provide_handlers_command(provider: Provider) -> None:
    provider.provide(source=CreateUser, scope=Scope.REQUEST)
    provider.provide(source=GetUserById, scope=Scope.REQUEST)
    provider.provide(source=GetUserByTelegramId, scope=Scope.REQUEST)
    provider.provide(source=BlockUser, scope=Scope.REQUEST)
    provider.provide(source=DeleteUser, scope=Scope.REQUEST)
    provider.provide(source=AddRegistrationCount, scope=Scope.REQUEST)
    provider.provide(source=CreateAuto, scope=Scope.REQUEST)
    provider.provide(source=GetAutoByNumber, scope=Scope.REQUEST)
    provider.provide(source=GetAutosByUserId, scope=Scope.REQUEST)
    provider.provide(source=DeleteAuto, scope=Scope.REQUEST)
    provider.provide(source=CheckSearchAccess, scope=Scope.REQUEST)
    provider.provide(source=CreateSearchTry, scope=Scope.REQUEST)
