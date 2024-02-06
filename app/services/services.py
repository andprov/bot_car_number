from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards.inline_keyboard import add_del_back_kb
from app.services.user_services import UserService
from app.utils import cmd, msg
from app.utils.msg import autos_msg

user_service = UserService()

AUTO_KB = add_del_back_kb(cmd.AUTO_ADD, cmd.AUTO_DEL, cmd.MAIN)


async def get_autos_menu(call: CallbackQuery, state: FSMContext) -> None:
    """Вывести меню управления автомобилями."""
    user = await user_service.get_user_with_auto(call.from_user.id)
    if user is None:
        await call.answer(msg.NO_DATA_MSG, True)
        return
    await call.message.edit_text(autos_msg(user.autos), reply_markup=AUTO_KB)
    await state.clear()
