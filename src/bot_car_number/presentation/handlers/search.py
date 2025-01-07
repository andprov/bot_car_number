from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot_car_number.adapters.postgres.gateways.auto import DatabaseAutoGateway
from bot_car_number.adapters.postgres.gateways.stats import DatabaseStatsGateway
from bot_car_number.adapters.postgres.gateways.user import DatabaseUserGateway
from bot_car_number.config_loader import SEARCH_COUNT_LIMIT
from bot_car_number.entities.stats import StatsData
from bot_car_number.presentation.handlers.states import SearchAuto
from bot_car_number.presentation.keyboards.inline_keyboard import back_kb
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.services.auto_service import AutoService
from bot_car_number.services.stats_service import StatsService
from bot_car_number.services.user_service import UserService

router = Router(name="search_commands-router")

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(StateFilter(None), F.data == cmd.SEARCH)
async def search(
    call: CallbackQuery,
    state: FSMContext,
    user_service: UserService,
    auto_service: AutoService,
    stats_service: StatsService,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
    stats_dao: DatabaseStatsGateway,
) -> None:
    """Обработчик перехода к поиску."""
    user = await user_service.get_user_by_telegram_id(
        user_dao, call.from_user.id
    )
    if not user:
        await call.answer(msg.NO_DATA_MSG, True)
        return

    if not await stats_service.check_search_access(stats_dao, user.id):
        await call.answer(msg.SEARCH_ACCESS_DENIED, True)
        return

    if not await auto_service.get_user_autos(auto_dao, user.id):
        await call.answer(msg.NO_AUTO_MSG, True)
        return

    await call.message.edit_text(
        msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
    )
    await state.update_data(user_id=user.id, search_count=1)
    await state.set_state(state=SearchAuto.enter_number)


@router.message(SearchAuto.enter_number)
async def enter_search_number(
    message: Message,
    state: FSMContext,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
    stats_dao: DatabaseStatsGateway,
    auto_service: AutoService,
    user_service: UserService,
    stats_service: StatsService,
) -> None:
    """Обработчик ввода номера автомобиля при поиске."""
    number = message.text.upper()
    if not auto_service.validate_number(number):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return

    data = await state.get_data()
    search_count = data["search_count"]
    if search_count > SEARCH_COUNT_LIMIT:
        await message.answer(msg.SEARCH_ACCESS_DENIED)
        await state.clear()
        return

    stats = StatsData(user_id=data["user_id"], number=number)
    await stats_service.add_search_try(stats_dao, stats)
    search_count += 1
    await state.update_data(search_count=search_count)

    auto = await auto_service.get_auto_by_number(auto_dao, number)
    if auto is None:
        await message.answer(msg.AUTO_NOT_EXIST_MSG, reply_markup=BACK_KB)
        return

    user = await user_service.get_user_by_telegram_id(
        user_dao, tg_id=message.from_user.id
    )

    if user.id == auto.user_id:
        await message.answer(msg.OWNER_YOUR_MSG)
        await state.clear()
        return

    owner = await user_service.get_user(user_dao, auto.user_id)
    if owner:
        await message.answer(msg.OWNER_MSG.format(owner.phone))
        await state.clear()
