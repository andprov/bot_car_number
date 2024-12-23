import re

from bot_car_number.dao.auto import DatabaseAutoGateway
from bot_car_number.entities.auto import Auto


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
    async def check_auto(cls, dao: DatabaseAutoGateway, number: str) -> bool:
        """Проверить наличие автомобиля в базе."""
        if await dao.find_one_or_none(number=number.upper()):
            return True
        return False

    @classmethod
    async def add_auto(cls, dao: DatabaseAutoGateway, **data) -> None:
        """Добавить автомобиль в базу."""
        await dao.add_auto(**data)

    @classmethod
    async def get_auto_by_number(
        cls, dao: DatabaseAutoGateway, number: str
    ) -> Auto | None:
        """Вернуть автомобиль и его владельца по номеру."""
        return await dao.get_auto_by_number(number=number)

    @classmethod
    async def delete_auto(cls, dao: DatabaseAutoGateway, id: int) -> None:
        """Удалить автомобиль из базы."""
        await dao.delete(id=id)

    # -->
    @classmethod
    async def get_user_autos(
        cls, dao: DatabaseAutoGateway, user_id: int
    ) -> list[Auto | None]:
        return await dao.get_user_autos(user_id=user_id)
