from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.use_case.add_registration_count import (
    AddRegistrationCount,
)
from bot_car_number.application.use_case.add_user import AddUser
from bot_car_number.application.use_case.block_user import BlockUser
from bot_car_number.application.use_case.delete_user import DeleteUser
from bot_car_number.presentation.keyboards.inline_keyboard import (
    confirm_kb,
    main_kb,
)
from bot_car_number.presentation.keyboards.reply_keyboard import contact_kb
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Button as btn
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.presentation.states import AddUserState

router = Router()


@router.callback_query(F.data == cmd.USER)
async def user_menu(call: CallbackQuery, user: UserDTO) -> None:
    keyboard = confirm_kb(btn.ADD_TXT, cmd.USER_ADD, cmd.MAIN)
    if user:
        keyboard = confirm_kb(btn.DELETE_TXT, cmd.USER_DEL, cmd.MAIN)

    await call.message.edit_text(
        text=msg.user_msg(user=user),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == cmd.USER_ADD)
async def create_user(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(
        text=msg.USER_CONTACT_MSG,
        reply_markup=contact_kb(),
    )

    await state.set_state(state=AddUserState.add_user_contact)


@router.message(AddUserState.add_user_contact, F.contact)
async def add_user_contact(
    message: Message,
    state: FSMContext,
    add_user: FromDishka[AddUser],
    add_registration_count: FromDishka[AddRegistrationCount],
    block_user: FromDishka[BlockUser],
) -> None:
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
    await add_user(user=user)

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
async def remove_user(call: CallbackQuery) -> None:
    await call.message.edit_text(
        text=msg.USER_DEL_CONFIRM_MSG,
        reply_markup=confirm_kb(
            btn.DEL_CONFIRM_TXT,
            cmd.USER_DEL_CONFIRM,
            cmd.USER,
        ),
    )


@router.callback_query(F.data == cmd.USER_DEL_CONFIRM)
async def delete_user_confirm(
    call: CallbackQuery,
    user: UserDTO,
    delete_user: FromDishka[DeleteUser],
) -> None:
    await delete_user(id=user.id)
    await call.message.edit_text(text=msg.USER_DELETE_MSG)
