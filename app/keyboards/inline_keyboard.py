from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils import cmd

BACK_TXT = "<< Назад"
DEL_CONFIRM_TXT = "Подтвердить Удаление"
USER_MENU_TXT = "Мои Данные"
AUTO_MENU_TXT = "Мои Автомобили"
SEARCH_TXT = "Поиск"
ADD_TXT = "Добавить"
DELETE_TXT = "Удалить"
SAVE_TXT = "Сохранить"


def get_btn(text: str, action: str) -> InlineKeyboardButton:
    """Вернуть кнопку."""
    return InlineKeyboardButton(text=text, callback_data=action)


def back_kb(back: str) -> InlineKeyboardMarkup:
    """Клавиатура возврата в предыдущее меню."""
    back_btn = get_btn(BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn]])


def save_kb(back: str) -> InlineKeyboardMarkup:
    """Клавиатура сохранения."""
    save_btn = get_btn(SAVE_TXT, cmd.AUTO_SAVE)
    back_btn = get_btn(BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[save_btn], [back_btn]])


def main_kb() -> InlineKeyboardMarkup:
    """Клавиатура главного меню."""
    user_menu_btn = get_btn(USER_MENU_TXT, cmd.USER)
    auto_menu_btn = get_btn(AUTO_MENU_TXT, cmd.AUTO_MENU)
    search_btn = get_btn(SEARCH_TXT, cmd.SEARCH)
    return InlineKeyboardMarkup(
        inline_keyboard=[[user_menu_btn, auto_menu_btn], [search_btn]]
    )


def confirm_del_kb(delete: str, back: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления."""
    delete_btn = get_btn(DEL_CONFIRM_TXT, delete)
    back_btn = get_btn(BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[delete_btn], [back_btn]])


def add_del_back_kb(add: str, delete: str, back: str) -> InlineKeyboardMarkup:
    """Клавиатура добавления, удаления, возврата."""
    add_btn = get_btn(ADD_TXT, add)
    delete_btn = get_btn(DELETE_TXT, delete)
    back_btn = get_btn(BACK_TXT, back)
    return InlineKeyboardMarkup(
        inline_keyboard=[[add_btn, delete_btn], [back_btn]]
    )
