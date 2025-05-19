from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_car_number.presentation.misc.cmd import Button as btn
from bot_car_number.presentation.misc.cmd import Command as cmd


def get_btn(text: str, action: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=action)


def back_kb(back: str) -> InlineKeyboardMarkup:
    back_btn = get_btn(btn.BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[back_btn]])


def main_kb() -> InlineKeyboardMarkup:
    user_menu_btn = get_btn(btn.USER_MENU_TXT, cmd.USER)
    auto_menu_btn = get_btn(btn.AUTO_MENU_TXT, cmd.AUTO_MENU)
    block_auto_btn = get_btn(btn.BLOCK_AUTO_TXT, cmd.BLOCK_AUTO)
    search_btn = get_btn(btn.SEARCH_TXT, cmd.SEARCH)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [user_menu_btn, auto_menu_btn],
            [block_auto_btn],
            [search_btn],
        ]
    )


def confirm_kb(text: str, confirm: str, back: str) -> InlineKeyboardMarkup:
    confirm_btn = get_btn(text, confirm)
    back_btn = get_btn(btn.BACK_TXT, back)
    return InlineKeyboardMarkup(inline_keyboard=[[confirm_btn], [back_btn]])


def add_del_back_kb(add: str, delete: str, back: str) -> InlineKeyboardMarkup:
    add_btn = get_btn(btn.ADD_TXT, add)
    delete_btn = get_btn(btn.DELETE_TXT, delete)
    back_btn = get_btn(btn.BACK_TXT, back)
    return InlineKeyboardMarkup(
        inline_keyboard=[[add_btn, delete_btn], [back_btn]]
    )
