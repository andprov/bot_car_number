from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.dao.user import UserDAO
from app.handlers.states import SearchAuto
from app.keyboards.inline_keyboard import back_kb
from app.services.services import get_auto
from app.utils import cmd, msg
from app.utils.validators import validate_number

router = Router(name="search_commands-router")

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(StateFilter(None), F.data == cmd.SEARCH)
async def search(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик перехода к поиску."""
    user = await UserDAO.find_all_user_autos(tg_id=call.from_user.id)
    if user:
        if user.autos:
            await call.message.edit_text(
                msg.ENTER_NUMBER_MSG, reply_markup=BACK_KB
            )
            await state.set_state(state=SearchAuto.enter_number)
            return
        await call.answer(msg.NO_AUTO_MSG, True)
    await call.answer(msg.NO_DATA_MSG, True)


@router.message(SearchAuto.enter_number)
async def enter_search_number(message: Message, state: FSMContext) -> None:
    """Обработчик ввода номера автомобиля при поиске."""
    if not await validate_number(message, cmd.MAIN):
        return
    auto = await get_auto(message, cmd.MAIN)
    if auto is None:
        return
    if auto.owner.tg_id == message.from_user.id:
        await message.answer(msg.OWNER_YOUR_MSG)
        await state.clear()
        return
    await message.answer(msg.OWNER_MSG.format(auto.owner.phone))
    await state.clear()
