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
async def cmd_menu(message: Message, state: FSMContext) -> None:
    """Обработчик command вызова главного меню."""
    await state.clear()
    await message.answer(msg.MAIN_MSG, reply_markup=main_kb())


@router.callback_query(F.data == cmd.MAIN)
async def callback_menu(call: CallbackQuery, state: FSMContext) -> None:
    """Обработчик callback вызова главного меню."""
    await state.clear()
    await call.message.edit_text(msg.MAIN_MSG, reply_markup=main_kb())


@router.message(Command(cmd.CANCEL))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """Обработчик command отмена."""
    await state.clear()
    await message.answer(msg.CANCEL_MSG, reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == cmd.CANCEL)
async def callback_cancel(call: CallbackQuery, state: FSMContext) -> None:
    """ "Обработчик callback отмена."""
    await state.clear()
    await call.message.edit_text(msg.CANCEL_MSG)
