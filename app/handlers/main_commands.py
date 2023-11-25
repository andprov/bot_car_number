from typing import Union

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.keyboards.inline_keyboard import main_kb
from app.services import cmd, msg

router = Router(name="main_menu-router")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработчик запуска бота."""
    text = msg.start_msg(message.from_user.first_name)
    await message.answer(text)


@router.message(Command(cmd.MAIN))
@router.callback_query(F.data == cmd.MAIN)
async def cmd_menu(
    call_or_message: Union[CallbackQuery, Message], state: FSMContext
) -> None:
    """Обработчик вызова главного меню."""
    await state.clear()
    if isinstance(call_or_message, Message):
        await call_or_message.answer(msg.MAIN_MSG, reply_markup=main_kb())
    else:
        await call_or_message.message.edit_text(
            msg.MAIN_MSG, reply_markup=main_kb()
        )


@router.message(Command(cmd.CANCEL))
@router.message(F.text.lower() == "отмена")
@router.callback_query(F.data == cmd.CANCEL)
async def cmd_cansel(
    call_or_message: Union[CallbackQuery, Message],
    state: FSMContext,
) -> None:
    """Обработчик команды отмены."""
    if await state.get_state() is None:
        return
    await state.clear()
    if isinstance(call_or_message, Message):
        await call_or_message.answer(
            msg.CANCEL_MSG, reply_markup=ReplyKeyboardRemove()
        )
    else:
        await call_or_message.message.edit_text(msg.CANCEL_MSG)
