import re

from aiogram.types import Message

from app.db.models import Auto
from app.keyboards.inline_keyboard import back_kb
from app.services import msg
from app.services.query import get_auto_and_owner_query


async def validate_number(message: Message, action: str) -> bool:
    """Проверка формата номера."""
    keyboard = back_kb(action)
    pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
    if pattern.match(message.text.upper()):
        return True
    await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=keyboard)
    return False


async def get_auto(message: Message, action: str) -> Auto | None:
    """Вернуть автомобиль и владельца."""
    auto = await get_auto_and_owner_query(message.text.upper())
    if auto is None:
        await message.answer(
            msg.AUTO_NOT_EXIST_MSG, reply_markup=back_kb(action)
        )
    return auto
