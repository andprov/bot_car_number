from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.states import SearchAuto
from app.keyboards.inline_keyboard import back_kb
from app.misc import cmd, msg
from app.services.auto_service import auto_service
from app.services.user_service import user_service

router = Router(name="search_commands-router")

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(StateFilter(None), F.data == cmd.SEARCH)
async def search(
    call: CallbackQuery, session: AsyncSession, state: FSMContext
) -> None:
    """Обработчик перехода к поиску."""
    user = await user_service.get_user_with_auto(
        session, tg_id=call.from_user.id
    )
    if user:
        if user.autos:
            await call.message.edit_text(
                msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
            )
            await state.set_state(state=SearchAuto.enter_number)
            return
        await call.answer(msg.NO_AUTO_MSG, True)
    await call.answer(msg.NO_DATA_MSG, True)


@router.message(SearchAuto.enter_number)
async def enter_search_number(
    message: Message, session: AsyncSession, state: FSMContext
) -> None:
    """Обработчик ввода номера автомобиля при поиске."""
    number = message.text.upper()
    if not auto_service.validate_number(number):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return
    auto = await auto_service.get_auto_with_owner(session, number)
    if auto is None:
        await message.answer(msg.AUTO_NOT_EXIST_MSG, reply_markup=BACK_KB)
        return
    if auto.owner.tg_id == message.from_user.id:
        await message.answer(msg.OWNER_YOUR_MSG)
        await state.clear()
        return
    await message.answer(msg.OWNER_MSG.format(auto.owner.phone))
    await state.clear()
