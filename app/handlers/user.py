from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.states import AddUser
from app.keyboards.inline_keyboard import (
    add_del_back_kb,
    confirm_del_kb,
    main_kb,
)
from app.keyboards.reply_keyboard import contact_kb
from app.misc import cmd, msg
from app.services.user_service import user_service

router = Router(name="user_commands-router")

USER_MENU_KEYBOARD = add_del_back_kb(cmd.USER_ADD, cmd.USER_DEL, cmd.MAIN)


@router.callback_query(F.data == cmd.USER)
async def user_menu(call: CallbackQuery) -> None:
    """Обработчик вызова меню управления данными пользователя."""
    await call.message.edit_text(msg.USER_MSG, reply_markup=USER_MENU_KEYBOARD)


@router.callback_query(F.data == cmd.USER_ADD)
async def add_user(
    call: CallbackQuery, session: AsyncSession, state: FSMContext
) -> None:
    """Обработчик нажатия кнопки добавления пользователя."""
    if await user_service.check_user(session, call.from_user.id):
        await call.answer(msg.USER_EXIST_MSG, True)
        return
    await call.message.delete()
    await call.message.answer(msg.USER_CONTACT_MSG, reply_markup=contact_kb())
    await state.set_state(AddUser.add_user_contact)


@router.message(AddUser.add_user_contact, F.contact)
async def add_user_contact(
    message: Message, session: AsyncSession, state: FSMContext
) -> None:
    """Обработчик ответа пользователя с контактными данными."""
    tg_id = message.from_user.id
    contact = message.contact
    if contact.user_id != tg_id:
        await message.answer(msg.USER_WRONG_MSG)
        return
    await user_service.add_user(session, contact)
    if await user_service.check_registration_limit(session, tg_id):
        await message.answer(
            msg.USER_MAX_COUNT_REGISTRATIONS_MSG,
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        await user_service.block_user(session, tg_id)
        return
    await message.answer(msg.USER_ADD_MSG, reply_markup=ReplyKeyboardRemove())
    await message.answer(msg.MAIN_MSG, reply_markup=main_kb())
    await state.clear()


@router.callback_query(F.data == cmd.USER_DEL)
async def delete_user(call: CallbackQuery, session: AsyncSession) -> None:
    """Обработчик нажатия кнопки удаления пользователя."""
    if await user_service.check_user(session, call.from_user.id):
        await call.message.edit_text(
            msg.USER_DEL_CONFIRM_MSG,
            reply_markup=confirm_del_kb(cmd.USER_DEL_CONFIRM, cmd.USER),
        )
        return
    await call.answer(msg.USER_NOT_EXIST_MSG, True)


@router.callback_query(F.data == cmd.USER_DEL_CONFIRM)
async def delete_user_confirm(
    call: CallbackQuery, session: AsyncSession
) -> None:
    """Обработчик подтверждения удаления пользователя и автомобилей из БД."""
    await user_service.delete_user(session, call.from_user.id)
    await call.message.edit_text(msg.USER_DELETE_MSG)
