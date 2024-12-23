from abc import abstractmethod
from typing import Protocol

from bot_car_number.entities.auto import Auto


class AutoGateway(Protocol):
    @abstractmethod
    async def add_auto(self, auto: Auto) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_auto_by_number(self, number: str) -> Auto | None:
        raise NotImplementedError

    @abstractmethod
    async def get_autos_by_user_id(self, user_id: int) -> list[Auto | None]:
        raise NotImplementedError

    @abstractmethod
    async def delete_auto(self, id: int) -> None:
        raise NotImplementedError
