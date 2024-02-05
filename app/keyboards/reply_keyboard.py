from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def contact_kb() -> ReplyKeyboardMarkup:
    """Клавиатура получения контактных данных пользователя."""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отправить", request_contact=True),
        KeyboardButton(text="Отмена"),
    )
    return builder.as_markup(resize_keyboard=True)
