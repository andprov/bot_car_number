from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.dao.auto import AutoDAO
from app.dao.user import UserDAO
from app.db.models import Auto
from app.keyboards.inline_keyboard import add_del_back_kb, back_kb
from app.utils import cmd, msg
from app.utils.msg import autos_msg

AUTO_KB = add_del_back_kb(cmd.AUTO_ADD, cmd.AUTO_DEL, cmd.MAIN)


async def get_autos_menu(call: CallbackQuery, state: FSMContext) -> None:
    """Вывести меню управления автомобилями."""
    user = await UserDAO.find_all_user_autos(tg_id=call.from_user.id)
    if user is None:
        await call.answer(msg.NO_DATA_MSG, True)
        return
    await call.message.edit_text(autos_msg(user.autos), reply_markup=AUTO_KB)
    await state.clear()


async def get_auto(message: Message, command: str) -> Auto | None:
    """Вернуть автомобиль по его номеру."""
    auto = await AutoDAO.find_auto_with_owner(number=message.text.upper())
    if auto is None:
        await message.answer(
            msg.AUTO_NOT_EXIST_MSG, reply_markup=back_kb(command)
        )
    return auto
