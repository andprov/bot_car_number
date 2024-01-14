from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import MAX_AUTO_COUNT, MAX_AUTO_NAME_LEN
from app.dao.auto import AutoDAO
from app.dao.user import UserDAO
from app.handlers.states import AddAuto, DeleteAuto
from app.keyboards.inline_keyboard import save_kb, confirm_del_kb, back_kb
from app.services.services import get_autos_menu
from app.utils import cmd, msg
from app.utils.validators import validate_number

router = Router(name="auto_commands-router")

BACK_KB = back_kb(cmd.AUTO_MENU)


@router.callback_query(F.data == cmd.AUTO_MENU)
async def auto_menu(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик вызова меню управления автомобилями пользователя."""
    await get_autos_menu(call, state)


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_ADD)
async def add_auto(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик перехода к добавлению автомобиля."""
    user = await UserDAO.find_all_user_autos(tg_id=call.from_user.id)
    if len(user.autos) >= MAX_AUTO_COUNT:
        await call.answer(msg.AUTO_MAX_COUNT_MSG, True)
        return
    await call.message.edit_text(msg.ENTER_NUMBER_MSG, reply_markup=BACK_KB)
    await state.update_data(user_id=user.id)
    await state.set_state(AddAuto.enter_number)


@router.message(AddAuto.enter_number)
async def add_number(message: Message, state: FSMContext) -> None:
    """Обработчик ввода номера автомобиля при добавлении."""
    if not await validate_number(message, cmd.AUTO_MENU):
        return
    if await AutoDAO.find_one_or_none(number=message.text.upper()):
        await message.answer(msg.AUTO_EXIST_MSG, reply_markup=BACK_KB)
        return
    await message.answer(msg.AUTO_ADD_MODEL_MSG, reply_markup=BACK_KB)
    await state.update_data(number=message.text.upper())
    await state.set_state(AddAuto.enter_model)


@router.message(AddAuto.enter_model)
async def add_model(message: Message, state: FSMContext) -> None:
    """Обработчик ввода марки автомобиля."""
    if len(message.text) > MAX_AUTO_NAME_LEN:
        await message.answer(msg.AUTO_MODEL_LONG_MSG, reply_markup=BACK_KB)
        return
    await state.update_data(model=message.text)
    data = await state.get_data()
    await message.answer(
        msg.AUTO_CHECK_DATA_MSG.format(data["number"], data["model"]),
        reply_markup=save_kb(cmd.AUTO_MENU),
    )
    await state.set_state(AddAuto.confirm)


@router.callback_query(AddAuto.confirm, F.data == cmd.AUTO_SAVE)
async def add_auto_confirm(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик подтверждения добавления автомобиля в БД."""
    data = await state.get_data()
    number, model, user_id = data["number"], data["model"], data["user_id"]
    if not await AutoDAO.find_one_or_none(number=number):
        await AutoDAO.add(number=number, model=model, owner_id=user_id)
    await get_autos_menu(call, state)


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_DEL)
async def del_auto(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик нажатия кнопки удаления автомобиля."""
    user = await UserDAO.find_all_user_autos(tg_id=call.from_user.id)
    if not user.autos:
        await call.answer(msg.AUTO_NONE_MSG, True)
        return
    await call.message.edit_text(msg.ENTER_NUMBER_MSG, reply_markup=BACK_KB)
    await state.set_state(state=DeleteAuto.enter_number)


@router.message(DeleteAuto.enter_number)
async def enter_number(message: Message, state: FSMContext) -> None:
    """Обработчик ввода номера автомобиля при удалении."""
    if not await validate_number(message, cmd.AUTO_MENU):
        return
    auto = await AutoDAO.find_auto_with_owner(number=message.text.upper())
    if auto is None:
        await message.answer(
            msg.AUTO_NOT_EXIST_MSG, reply_markup=back_kb(cmd.AUTO_MENU)
        )
        return
    if auto.owner.tg_id != message.from_user.id:
        await message.answer(msg.AUTO_NOT_YOURS_MSG, reply_markup=BACK_KB)
        return
    keyboard = confirm_del_kb(cmd.AUTO_DEL_CONFIRM, cmd.AUTO_MENU)
    await state.update_data(auto=auto)
    await message.answer(msg.AUTO_DEL_CONFIRM_MSG, reply_markup=keyboard)
    await state.set_state(DeleteAuto.confirm)


@router.callback_query(DeleteAuto.confirm, F.data == cmd.AUTO_DEL_CONFIRM)
async def del_auto_confirm(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик подтверждения удаления автомобиля из БД."""
    data = await state.get_data()
    auto = data["auto"]
    if auto:
        await AutoDAO.delete(id=auto.id)
    await get_autos_menu(call, state)
