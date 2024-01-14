from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardRemove,
)

from app.dao.user import UserDAO
from app.handlers.states import AddUser
from app.keyboards.inline_keyboard import (
    confirm_del_kb,
    main_kb,
    add_del_back_kb,
)
from app.keyboards.reply_keyboard import contact_kb
from app.utils import cmd, msg

router = Router(name="user_commands-router")

USER_MENU_KEYBOARD = add_del_back_kb(cmd.USER_ADD, cmd.USER_DEL, cmd.MAIN)


@router.callback_query(F.data == cmd.USER)
async def user_menu(call: CallbackQuery) -> None:
    """Обработчик вызова меню управления данными пользователя."""
    await call.message.edit_text(msg.USER_MSG, reply_markup=USER_MENU_KEYBOARD)


@router.callback_query(F.data == cmd.USER_ADD)
async def add_user(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик нажатия кнопки добавления пользователя."""
    user = await UserDAO.find_one_or_none(tg_id=call.from_user.id)
    if user:
        await call.answer(msg.USER_EXIST_MSG, True)
        return
    await call.message.delete()
    await call.message.answer(msg.USER_CONTACT_MSG, reply_markup=contact_kb())
    await state.set_state(AddUser.add_user_contact)


@router.message(AddUser.add_user_contact, F.contact)
async def add_user_contact(message: Message, state: FSMContext) -> None:
    """Обработчик ответа пользователя с контактными данными."""
    if message.contact.user_id != message.from_user.id:
        await message.answer(msg.USER_WRONG_MSG)
        return
    await UserDAO.add(
        tg_id=message.contact.user_id,
        first_name=message.contact.first_name,
        phone=message.contact.phone_number,
    )
    await message.answer(msg.USER_ADD_MSG, reply_markup=ReplyKeyboardRemove())
    await message.answer(msg.MAIN_MSG, reply_markup=main_kb())
    await state.clear()


@router.callback_query(F.data == cmd.USER_DEL)
async def del_user(call: CallbackQuery) -> None:
    """Обработчик нажатия кнопки удаления пользователя."""
    user = await UserDAO.find_one_or_none(tg_id=call.from_user.id)
    if user:
        await call.message.edit_text(
            msg.USER_DEL_CONFIRM_MSG,
            reply_markup=confirm_del_kb(cmd.USER_DEL_CONFIRM, cmd.USER),
        )
        return
    await call.answer(msg.USER_NOT_EXIST_MSG, True)


@router.callback_query(F.data == cmd.USER_DEL_CONFIRM)
async def del_user_confirm(call: CallbackQuery) -> None:
    """Обработчик подтверждения удаления пользователя и автомобилей из БД."""
    await UserDAO.delete(tg_id=call.from_user.id)
    await call.message.edit_text(msg.USER_DELETE_MSG)
