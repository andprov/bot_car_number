import re

from aiogram.types import Message

from app.keyboards.inline_keyboard import back_kb
from app.utils import msg


async def validate_number(message: Message, action: str) -> bool:
    """Проверка формата номера."""
    keyboard = back_kb(action)
    pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
    if pattern.match(message.text.upper()):
        return True
    await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=keyboard)
    return False
