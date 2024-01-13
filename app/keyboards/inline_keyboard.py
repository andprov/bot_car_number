from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services import cmd


BACK_TXT = "<< Назад"
CANCEL_TXT = "Отмена"
DEL_CONFIRM_TXT = "Подтвердить Удаление"
USER_MENU_TXT = "Мои Данные"
AUTO_MENU_TXT = "Мои Автомобили"
SEARCH_TXT = "Поиск"
ADD_TXT = "Добавить"
DELETE_TXT = "Удалить"
SAVE_TXT = "Сохранить"


user_menu_btn = InlineKeyboardButton(
    text=USER_MENU_TXT, callback_data=cmd.USER
)
auto_menu_btn = InlineKeyboardButton(
    text=AUTO_MENU_TXT, callback_data=cmd.AUTO_MENU
)
search_btn = InlineKeyboardButton(text=SEARCH_TXT, callback_data=cmd.SEARCH)
cancel_btn = InlineKeyboardButton(text=CANCEL_TXT, callback_data=cmd.CANCEL)
save_btn = InlineKeyboardButton(text=SAVE_TXT, callback_data=cmd.AUTO_SAVE)


def add_btn(action: str) -> InlineKeyboardButton:
    """Кнопка добавления."""
    return InlineKeyboardButton(text=ADD_TXT, callback_data=action)


def delete_btn(action: str) -> InlineKeyboardButton:
    """Кнопка удаления."""
    return InlineKeyboardButton(text=DELETE_TXT, callback_data=action)


def del_confirm_btn(action: str) -> InlineKeyboardButton:
    """Кнопка подтверждения удаления."""
    return InlineKeyboardButton(text=DEL_CONFIRM_TXT, callback_data=action)


def back_btn(action: str) -> InlineKeyboardButton:
    """Кнопка предыдущего меню."""
    return InlineKeyboardButton(text=BACK_TXT, callback_data=action)


def back_kb(action: str) -> InlineKeyboardMarkup:
    """Клавиатура возврата в предыдущее меню."""
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn(action)]])


def cancel_kb() -> InlineKeyboardMarkup:
    """Клавиатура отмены."""
    return InlineKeyboardMarkup(inline_keyboard=[[cancel_btn]])


def save_kb(action: str) -> InlineKeyboardMarkup:
    """Клавиатура сохранения."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[save_btn], [back_btn(action)]]
    )


def main_kb() -> InlineKeyboardMarkup:
    """Клавиатура главного меню."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[user_menu_btn, auto_menu_btn], [search_btn]]
    )


def confirm_del_kb(action: str, back: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[del_confirm_btn(action)], [back_btn(back)]]
    )


def add_del_back_kb(add: str, delete: str, back: str) -> InlineKeyboardMarkup:
    """Клавиатура добавления, удаления, возврата."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[add_btn(add), delete_btn(delete)], [back_btn(back)]]
    )
