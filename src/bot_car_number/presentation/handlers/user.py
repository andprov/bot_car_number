from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from dishka.integrations.aiogram import FromDishka, inject

from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.use_case.add_registration_count import (
    AddRegistrationCount,
)
from bot_car_number.application.use_case.block_user import BlockUser
from bot_car_number.application.use_case.create_user import CreateUser
from bot_car_number.application.use_case.delete_user import DeleteUser
from bot_car_number.application.use_case.get_user_by_telegram_id import (
    GetUserByTelegramId,
)
from bot_car_number.presentation.handlers.states import AddUser
from bot_car_number.presentation.keyboards.inline_keyboard import (
    add_back_kb,
    confirm_del_kb,
    del_back_btn,
    main_kb,
)
from bot_car_number.presentation.keyboards.reply_keyboard import contact_kb
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Command as cmd

router = Router()

USER_MENU_ADD_KEYBOARD = add_back_kb(cmd.USER_ADD, cmd.MAIN)
USER_MENU_DELETE_KEYBOARD = del_back_btn(cmd.USER_DEL, cmd.MAIN)


@router.callback_query(F.data == cmd.USER)
@inject
async def user_menu(
    call: CallbackQuery,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
) -> None:
    """Вызов меню управления данными пользователя."""
    keyboard = USER_MENU_ADD_KEYBOARD
    user = await get_user_by_telegram_id(tg_id=call.from_user.id)
    if user:
        keyboard = USER_MENU_DELETE_KEYBOARD

    await call.message.edit_text(
        text=msg.user_msg(user=user),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == cmd.USER_ADD)
@inject
async def add_user(
    call: CallbackQuery,
    state: FSMContext,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
) -> None:
    """Нажатие кнопки добавления пользователя."""
    if await get_user_by_telegram_id(tg_id=call.from_user.id):
        await call.answer(text=msg.USER_EXIST_MSG, show_alert=True)
        return

    await call.message.delete()
    await call.message.answer(
        text=msg.USER_CONTACT_MSG,
        reply_markup=contact_kb(),
    )
    await state.set_state(state=AddUser.add_user_contact)


@router.message(AddUser.add_user_contact, F.contact)
@inject
async def add_user_contact(
    message: Message,
    state: FSMContext,
    create_user: FromDishka[CreateUser],
    add_registration_count: FromDishka[AddRegistrationCount],
    block_user: FromDishka[BlockUser],
) -> None:
    """Обработчик ответа пользователя с контактными данными."""
    tg_id = message.from_user.id
    contact = message.contact
    if contact.user_id != tg_id:
        await message.answer(text=msg.USER_WRONG_MSG)
        return

    user = UserDTO(
        id=None,
        tg_id=contact.user_id,
        first_name=contact.first_name,
        phone=contact.phone_number,
        active=True,
    )
    await create_user(user=user)

    if not await add_registration_count(tg_id=tg_id):
        await message.answer(
            text=msg.USER_MAX_COUNT_REGISTRATIONS_MSG,
            reply_markup=ReplyKeyboardRemove(),
        )
        await block_user(tg_id=tg_id)
        await state.clear()
        return

    await message.answer(
        text=msg.USER_ADD_MSG,
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        text=msg.MAIN_MSG,
        reply_markup=main_kb(),
    )
    await state.clear()


@router.callback_query(F.data == cmd.USER_DEL)
@inject
async def delete_user(
    call: CallbackQuery,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
) -> None:
    """Нажатие кнопки удаления пользователя."""
    if await get_user_by_telegram_id(tg_id=call.from_user.id):
        await call.message.edit_text(
            text=msg.USER_DEL_CONFIRM_MSG,
            reply_markup=confirm_del_kb(cmd.USER_DEL_CONFIRM, cmd.USER),
        )
        return

    await call.answer(text=msg.USER_NOT_EXIST_MSG, show_alert=True)


@router.callback_query(F.data == cmd.USER_DEL_CONFIRM)
@inject
async def delete_user_confirm(
    call: CallbackQuery,
    delete_user: FromDishka[DeleteUser],
) -> None:
    """Подтверждение удаления пользователя и автомобилей из БД."""
    await delete_user(tg_id=call.from_user.id)
    await call.message.edit_text(text=msg.USER_DELETE_MSG)
