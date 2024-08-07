from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from bot_car_number.dao.user import UserDAO
from bot_car_number.keyboards.inline_keyboard import add_del_back_kb, main_kb
from bot_car_number.misc import msg
from bot_car_number.misc.cmd import Button as btn
from bot_car_number.misc.cmd import Command as cmd
from bot_car_number.services.user_service import UserService

router = Router(name="main_menu-router")

AUTO_KB = add_del_back_kb(cmd.AUTO_ADD, cmd.AUTO_DEL, cmd.MAIN)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработчик запуска бота."""
    text = msg.start_msg(message.from_user.first_name)
    await message.answer(text)


@router.message(Command(cmd.MAIN))
@router.callback_query(F.data == cmd.MAIN)
async def cmd_menu(
    call_or_message: CallbackQuery | Message,
    state: FSMContext,
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
@router.message(F.text == btn.CANCEL_TXT)
@router.callback_query(F.data == cmd.CANCEL)
async def cmd_cancel(
    call_or_message: CallbackQuery | Message,
    state: FSMContext,
) -> None:
    """Обработчик команды отмены."""
    if await state.get_state():
        await state.clear()
        if isinstance(call_or_message, Message):
            await call_or_message.answer(
                msg.CANCEL_MSG, reply_markup=ReplyKeyboardRemove()
            )
        else:
            await call_or_message.message.edit_text(msg.CANCEL_MSG)
    else:
        await call_or_message.answer(
            msg.STATE_CLEAR, reply_markup=ReplyKeyboardRemove()
        )


async def get_autos_menu(
    call: CallbackQuery,
    state: FSMContext,
    user_dao: UserDAO,
) -> None:
    """Обработчик вызова меню управления автомобилями."""
    user = await UserService.get_user_with_auto(user_dao, call.from_user.id)
    if user is None:
        await call.answer(msg.NO_DATA_MSG, True)
        return
    await call.message.edit_text(
        msg.autos_msg(user.autos), reply_markup=AUTO_KB
    )
    await state.clear()
