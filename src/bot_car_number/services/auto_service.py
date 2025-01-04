import re

from bot_car_number.adapters.db.gateways.auto import DatabaseAutoGateway
from bot_car_number.entities.auto import Auto


class AutoService:
    @classmethod
    def validate_number(cls, number: str) -> bool:
        pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
        if pattern.match(number):
            return True
        return False

    @classmethod
    async def add_auto(cls, dao: DatabaseAutoGateway, auto: Auto) -> None:
        await dao.add_auto(auto)

    @classmethod
    async def get_auto_by_number(
        cls, dao: DatabaseAutoGateway, number: str
    ) -> Auto | None:
        return await dao.get_auto_by_number(number=number)

    @classmethod
    async def get_user_autos(
        cls, dao: DatabaseAutoGateway, user_id: int
    ) -> list[Auto | None]:
        return await dao.get_autos_by_user_id(user_id=user_id)

    @classmethod
    async def delete_auto(cls, dao: DatabaseAutoGateway, id: int) -> None:
        await dao.delete_auto(id=id)
