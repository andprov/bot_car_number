from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.misc import cmd


def get_btn(text: str, action: str) -> InlineKeyboardButton:
    """Вернуть кнопку."""
    return InlineKeyboardButton(text=text, callback_data=action)


def back_kb(back: str) -> InlineKeyboardMarkup:
    """Клавиатура возврата в предыдущее меню."""
    back_btn = get_btn(cmd.BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn]])


def save_kb(back: str) -> InlineKeyboardMarkup:
    """Клавиатура сохранения."""
    save_btn = get_btn(cmd.SAVE_TXT, cmd.AUTO_SAVE)
    back_btn = get_btn(cmd.BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[save_btn], [back_btn]])


def main_kb() -> InlineKeyboardMarkup:
    """Клавиатура главного меню."""
    user_menu_btn = get_btn(cmd.USER_MENU_TXT, cmd.USER)
    auto_menu_btn = get_btn(cmd.AUTO_MENU_TXT, cmd.AUTO_MENU)
    search_btn = get_btn(cmd.SEARCH_TXT, cmd.SEARCH)
    return InlineKeyboardMarkup(
        inline_keyboard=[[user_menu_btn, auto_menu_btn], [search_btn]]
    )


def confirm_del_kb(delete: str, back: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления."""
    delete_btn = get_btn(cmd.DEL_CONFIRM_TXT, delete)
    back_btn = get_btn(cmd.BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[delete_btn], [back_btn]])


def add_del_back_kb(add: str, delete: str, back: str) -> InlineKeyboardMarkup:
    """Клавиатура добавления, удаления, возврата."""
    add_btn = get_btn(cmd.ADD_TXT, add)
    delete_btn = get_btn(cmd.DELETE_TXT, delete)
    back_btn = get_btn(cmd.BACK_TXT, back)
    return InlineKeyboardMarkup(
        inline_keyboard=[[add_btn, delete_btn], [back_btn]]
    )
