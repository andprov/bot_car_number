from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka, inject

from bot_car_number.application.use_case.check_search_access import (
    CheckSearchAccess,
)
from bot_car_number.application.use_case.get_autos_by_user_id import (
    GetAutosByUserId,
)
from bot_car_number.application.use_case.get_user_by_telegram_id import (
    GetUserByTelegramId,
)
from bot_car_number.application.use_case.search_auto import GetAutoOwnerData
from bot_car_number.presentation.handlers.states import SearchAuto
from bot_car_number.presentation.keyboards.inline_keyboard import back_kb
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Command as cmd

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
async def enter_number(
    message: Message,
    state: FSMContext,
    get_auto_owner_data: FromDishka[GetAutoOwnerData],
) -> None:
    """Ввод номера автомобиля при поиске."""
    msg, clear_state = await get_auto_owner_data(
        number=message.text.upper(),
        tg_id=message.from_user.id,
    )

    if clear_state:
        await message.answer(text=msg)
        await state.clear()
        return

    await message.answer(text=msg, reply_markup=BACK_KB)
    return
