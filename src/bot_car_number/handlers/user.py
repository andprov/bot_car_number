from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot_car_number.dao.registration import RegDAO
from bot_car_number.dao.user import DatabaseUserGateway
from bot_car_number.entities.user import User
from bot_car_number.handlers.states import AddUser
from bot_car_number.keyboards.inline_keyboard import (
    add_back_kb,
    confirm_del_kb,
    del_back_btn,
    main_kb,
)
from bot_car_number.keyboards.reply_keyboard import contact_kb
from bot_car_number.misc import msg
from bot_car_number.misc.cmd import Command as cmd
from bot_car_number.services.user_service import UserService

router = Router(name="user_commands-router")

USER_MENU_ADD_KEYBOARD = add_back_kb(cmd.USER_ADD, cmd.MAIN)
USER_MENU_DELETE_KEYBOARD = del_back_btn(cmd.USER_DEL, cmd.MAIN)


@router.callback_query(F.data == cmd.USER)
async def user_menu(
    call: CallbackQuery,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
) -> None:
    """Обработчик вызова меню управления данными пользователя."""
    keyboard = USER_MENU_ADD_KEYBOARD
    user = await user_service.get_user_by_telegram_id(
        user_dao, call.from_user.id
    )
    if user:
        keyboard = USER_MENU_DELETE_KEYBOARD
    await call.message.edit_text(msg.user_msg(user), reply_markup=keyboard)


@router.callback_query(F.data == cmd.USER_ADD)
async def add_user(
    call: CallbackQuery,
    state: FSMContext,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
) -> None:
    """Обработчик нажатия кнопки добавления пользователя."""
    if await user_service.get_user_by_telegram_id(user_dao, call.from_user.id):
        await call.answer(msg.USER_EXIST_MSG, True)
        return
    await call.message.delete()
    await call.message.answer(msg.USER_CONTACT_MSG, reply_markup=contact_kb())
    await state.set_state(AddUser.add_user_contact)


@router.message(AddUser.add_user_contact, F.contact)
async def add_user_contact(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
    registration_dao: RegDAO,
) -> None:
    """Обработчик ответа пользователя с контактными данными."""
    tg_id = message.from_user.id
    contact = message.contact
    if contact.user_id != tg_id:
        await message.answer(msg.USER_WRONG_MSG)
        return
    user = User(
        id=None,
        tg_id=contact.user_id,
        first_name=contact.first_name,
        phone=contact.phone_number,
        banned=False,
    )
    await user_service.add_user(user_dao, user)
    if await user_service.check_registration_limit(registration_dao, tg_id):
        await message.answer(
            msg.USER_MAX_COUNT_REGISTRATIONS_MSG,
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        await user_service.block_user(user_dao, tg_id)
        return
    await message.answer(msg.USER_ADD_MSG, reply_markup=ReplyKeyboardRemove())
    await message.answer(msg.MAIN_MSG, reply_markup=main_kb())
    await state.clear()


@router.callback_query(F.data == cmd.USER_DEL)
async def delete_user(
    call: CallbackQuery,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
) -> None:
    """Обработчик нажатия кнопки удаления пользователя."""
    if await user_service.get_user_by_telegram_id(user_dao, call.from_user.id):
        await call.message.edit_text(
            msg.USER_DEL_CONFIRM_MSG,
            reply_markup=confirm_del_kb(cmd.USER_DEL_CONFIRM, cmd.USER),
        )
        return
    await call.answer(msg.USER_NOT_EXIST_MSG, True)


@router.callback_query(F.data == cmd.USER_DEL_CONFIRM)
async def delete_user_confirm(
    call: CallbackQuery,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
) -> None:
    """Обработчик подтверждения удаления пользователя и автомобилей из БД."""
    await user_service.delete_user(user_dao, call.from_user.id)
    await call.message.edit_text(msg.USER_DELETE_MSG)
