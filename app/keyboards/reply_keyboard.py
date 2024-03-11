from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.misc import cmd


def contact_kb() -> ReplyKeyboardMarkup:
    """Клавиатура получения контактных данных пользователя."""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=cmd.CANSEL_TXT),
        KeyboardButton(text=cmd.SEND_TXT, request_contact=True),
    )
    return builder.as_markup(resize_keyboard=True)
