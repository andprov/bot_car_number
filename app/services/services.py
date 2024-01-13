from app.dao.user import UserDAO
from app.keyboards.inline_keyboard import add_del_back_kb
from app.utils.msg import autos_msg
from app.utils import cmd, msg

AUTO_KB = add_del_back_kb(cmd.AUTO_ADD, cmd.AUTO_DEL, cmd.MAIN)


async def get_autos_menu(call, state):
    user = await UserDAO.find_all_user_autos(tg_id=call.from_user.id)
    if user is None:
        await call.answer(msg.NO_DATA_MSG, True)
        return
    await call.message.edit_text(autos_msg(user.autos), reply_markup=AUTO_KB)
    await state.clear()
