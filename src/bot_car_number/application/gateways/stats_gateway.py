from abc import abstractmethod
from typing import Protocol

from bot_car_number.entities.stats import Stats


class StatsGateway(Protocol):
    @abstractmethod
    async def add_search_try(self, stats: Stats) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_search_count(self, user_id: int) -> int:
        raise NotADirectoryError
