from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka, inject

from bot_car_number.application.dto.stats import StatsDTO
from bot_car_number.application.use_case.check_search_access import (
    CheckSearchAccess,
)
from bot_car_number.application.use_case.create_search_try import (
    CreateSearchTry,
)
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
from bot_car_number.presentation.handlers.states import SearchAuto
from bot_car_number.presentation.keyboards.inline_keyboard import back_kb
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.services.auto_service import AutoService

router = Router()

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(StateFilter(None), F.data == cmd.SEARCH)
@inject
async def search(
    call: CallbackQuery,
    state: FSMContext,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
    check_search_access: FromDishka[CheckSearchAccess],
) -> None:
    """Переход к поиску."""
    user = await get_user_by_telegram_id(tg_id=call.from_user.id)
    if not user:
        await call.answer(text=msg.NO_DATA_MSG, show_alert=True)
        return

    if not await check_search_access(user_id=user.id):
        await call.answer(text=msg.SEARCH_ACCESS_DENIED, show_alert=True)
        return

    if not await get_autos_by_user_id(user_id=user.id):
        await call.answer(text=msg.NO_AUTO_MSG, show_alert=True)
        return

    await call.message.edit_text(
        text=msg.AUTO_ENTER_NUMBER_MSG,
        reply_markup=BACK_KB,
    )
    await state.set_state(state=SearchAuto.enter_number)


@router.message(SearchAuto.enter_number)
@inject
async def enter_search_number(
    message: Message,
    state: FSMContext,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
    get_user_by_id: FromDishka[GetUserById],
    get_auto_by_number: FromDishka[GetAutoByNumber],
    add_search_try: FromDishka[CreateSearchTry],
    check_search_access: FromDishka[CheckSearchAccess],
    # TODO: fix
    auto_service: AutoService,
) -> None:
    """Ввод номера автомобиля при поиске."""
    number = message.text.upper()
    if not auto_service.validate_number(number=number):
        await message.answer(
            text=msg.AUTO_FORMAT_ERR_MSG,
            reply_markup=BACK_KB,
        )
        return

    user = await get_user_by_telegram_id(tg_id=message.from_user.id)
    if not await check_search_access(user_id=user.id):
        await message.answer(text=msg.SEARCH_ACCESS_DENIED)
        await state.clear()
        return

    stats = StatsDTO(user_id=user.id, number=number)
    await add_search_try(stats=stats)

    auto = await get_auto_by_number(number=number)
    if auto is None:
        await message.answer(text=msg.AUTO_NOT_EXIST_MSG, reply_markup=BACK_KB)
        return

    if user.id == auto.user_id:
        await message.answer(text=msg.OWNER_YOUR_MSG)
        await state.clear()
        return

    owner = await get_user_by_id(user_id=auto.user_id)
    if owner:
        await message.answer(text=msg.OWNER_MSG.format(owner.phone))
        await state.clear()
        return
