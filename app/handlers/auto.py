from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import MAX_AUTO_COUNT, MAX_AUTO_NAME_LEN
from app.handlers.menu import get_autos_menu
from app.handlers.states import AddAuto, DeleteAuto
from app.keyboards.inline_keyboard import back_kb, confirm_del_kb, save_kb
from app.services.auto_service import AutoService
from app.services.user_service import UserService
from app.utils import cmd, msg

router = Router(name="auto_commands-router")

BACK_KB = back_kb(cmd.AUTO_MENU)


@router.callback_query(F.data == cmd.AUTO_MENU)
async def auto_menu(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик вызова меню управления автомобилями пользователя."""
    await get_autos_menu(call, state)


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_ADD)
async def add_auto(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик перехода к добавлению автомобиля."""
    user = await UserService.get_user_with_auto(call.from_user.id)
    if user:
        if len(user.autos) >= MAX_AUTO_COUNT:
            await call.answer(msg.AUTO_MAX_COUNT_MSG, True)
            return
        await call.message.edit_text(
            msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
        )
        await state.update_data(user_id=user.id)
        await state.set_state(AddAuto.enter_number)


@router.message(AddAuto.enter_number)
async def add_number(message: Message, state: FSMContext) -> None:
    """Обработчик ввода номера автомобиля при добавлении."""
    number = message.text.upper()
    if not AutoService.validate_number(number):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return
    if await AutoService.check_auto(number):
        await message.answer(msg.AUTO_EXIST_MSG, reply_markup=BACK_KB)
        return
    await message.answer(msg.AUTO_ADD_MODEL_MSG, reply_markup=BACK_KB)
    await state.update_data(number=number)
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
    if not await AutoService.check_auto(data["number"]):
        await AutoService.add_auto(**data)
    await get_autos_menu(call, state)


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_DEL)
async def del_auto(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик нажатия кнопки удаления автомобиля."""
    user = await UserService.get_user_with_auto(call.from_user.id)
    if user:
        if not user.autos:
            await call.answer(msg.AUTO_NONE_MSG, True)
            return
        await call.message.edit_text(
            msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
        )
        await state.set_state(state=DeleteAuto.enter_number)


@router.message(DeleteAuto.enter_number)
async def enter_number(message: Message, state: FSMContext) -> None:
    """Обработчик ввода номера автомобиля при удалении."""
    if not AutoService.validate_number(message.text):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return
    auto = await AutoService.get_auto_with_owner(message.text.upper())
    if auto is None:
        await message.answer(msg.AUTO_NOT_EXIST_MSG, reply_markup=BACK_KB)
        return
    if auto.owner.tg_id != message.from_user.id:
        await message.answer(msg.AUTO_NOT_YOURS_MSG, reply_markup=BACK_KB)
        return
    keyboard = confirm_del_kb(cmd.AUTO_DEL_CONFIRM, cmd.AUTO_MENU)
    await state.update_data(auto_id=auto.id)
    await message.answer(msg.AUTO_DEL_CONFIRM_MSG, reply_markup=keyboard)
    await state.set_state(DeleteAuto.confirm)


@router.callback_query(DeleteAuto.confirm, F.data == cmd.AUTO_DEL_CONFIRM)
async def del_auto_confirm(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик подтверждения удаления автомобиля из БД."""
    data = await state.get_data()
    auto_id = data.get("auto_id")
    if auto_id:
        await AutoService.delete_auto(auto_id)
    await get_autos_menu(call, state)
