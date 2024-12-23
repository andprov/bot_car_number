from abc import abstractmethod
from typing import Protocol

from bot_car_number.entities.auto import Auto


class AutoGateway(Protocol):
    @abstractmethod
    async def get_user_autos(self, user_id: int) -> list[Auto | None]:
        raise NotImplementedError
