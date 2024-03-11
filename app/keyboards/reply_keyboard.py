from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.misc.cmd import Button as btn


def contact_kb() -> ReplyKeyboardMarkup:
    """Клавиатура получения контактных данных пользователя."""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=btn.CANCEL_TXT),
        KeyboardButton(text=btn.SEND_TXT, request_contact=True),
    )
    return builder.as_markup(resize_keyboard=True)
