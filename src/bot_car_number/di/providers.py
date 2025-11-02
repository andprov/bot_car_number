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
from bot_car_number.adapters.postgres.gateways.search import (
    DatabaseSearchAttemptGateway,
)
from bot_car_number.adapters.postgres.gateways.user import DatabaseUserGateway
from bot_car_number.adapters.postgres.main import (
    get_async_sessionmaker,
    get_session,
)
from bot_car_number.application.interfaces.auto import AutoGateway
from bot_car_number.application.interfaces.registration import (
    RegistrationGateway,
)
from bot_car_number.application.interfaces.search import SearchAttemptGateway
from bot_car_number.application.interfaces.user import UserGateway
from bot_car_number.application.usecases.add_auto import AddAuto
from bot_car_number.application.usecases.add_auto_model import AddAutoModel
from bot_car_number.application.usecases.add_auto_number import AddAutoNumber
from bot_car_number.application.usecases.add_registration_count import (
    AddRegistrationCount,
)
from bot_car_number.application.usecases.add_search_attempt import (
    AddSearchAttempt,
)
from bot_car_number.application.usecases.add_user import AddUser
from bot_car_number.application.usecases.block_user import BlockUser
from bot_car_number.application.usecases.check_add_auto import (
    CheckUserAutosCount,
)
from bot_car_number.application.usecases.check_search_access import (
    CheckSearchAccess,
)
from bot_car_number.application.usecases.delete_auto import DeleteAuto
from bot_car_number.application.usecases.delete_user import DeleteUser
from bot_car_number.application.usecases.get_auto import GetAuto
from bot_car_number.application.usecases.get_auto_for_delete import (
    GetAutoForDelete,
)
from bot_car_number.application.usecases.get_autos_by_user_id import (
    GetAutosByUserId,
)
from bot_car_number.application.usecases.get_user import GetUser
from bot_car_number.application.usecases.get_user_by_telegram_id import (
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
        source=DatabaseSearchAttemptGateway,
        scope=Scope.REQUEST,
        provides=SearchAttemptGateway,
    )
    provider.provide(
        source=DatabaseRegistrationGateway,
        scope=Scope.REQUEST,
        provides=RegistrationGateway,
    )


def provide_handlers_command(provider: Provider) -> None:
    provider.provide(source=AddUser, scope=Scope.REQUEST)
    provider.provide(source=GetUser, scope=Scope.REQUEST)
    provider.provide(source=GetUserByTelegramId, scope=Scope.REQUEST)
    provider.provide(source=BlockUser, scope=Scope.REQUEST)
    provider.provide(source=DeleteUser, scope=Scope.REQUEST)
    provider.provide(source=AddRegistrationCount, scope=Scope.REQUEST)
    provider.provide(source=AddSearchAttempt, scope=Scope.REQUEST)
    provider.provide(source=CheckUserAutosCount, scope=Scope.REQUEST)
    provider.provide(source=AddAutoNumber, scope=Scope.REQUEST)
    provider.provide(source=AddAutoModel, scope=Scope.REQUEST)
    provider.provide(source=GetAuto, scope=Scope.REQUEST)
    provider.provide(source=GetAutoForDelete, scope=Scope.REQUEST)
    provider.provide(source=AddAuto, scope=Scope.REQUEST)
    provider.provide(source=GetAutosByUserId, scope=Scope.REQUEST)
    provider.provide(source=DeleteAuto, scope=Scope.REQUEST)
    provider.provide(source=CheckSearchAccess, scope=Scope.REQUEST)
