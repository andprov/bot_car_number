import re

from app.dao.auto import AutoDAO
from app.db.models import Auto


class AutoService:
    """Сервис для работы с автомобилями."""

    @classmethod
    def validate_number(cls, number: str) -> bool:
        """Проверка формата номера."""
        pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
        if pattern.match(number):
            return True
        return False

    @classmethod
    async def check_auto(cls, dao: AutoDAO, number: str) -> bool:
        """Проверить наличие автомобиля в базе."""
        if await dao.find_one_or_none(number=number.upper()):
            return True
        return False

    @classmethod
    async def add_auto(cls, dao: AutoDAO, **data) -> None:
        """Добавить автомобиль в базу."""
        await dao.add(**data)

    @classmethod
    async def get_auto(cls, dao: AutoDAO, number: str) -> Auto | None:
        """Вернуть автомобиль и его владельца по номеру."""
        return await dao.find_auto_with_owner(number=number)

    @classmethod
    async def delete_auto(cls, dao: AutoDAO, id: int) -> None:
        """Удалить автомобиль из базы."""
        await dao.delete(id=id)
