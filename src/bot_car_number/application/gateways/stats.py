from abc import abstractmethod
from typing import Protocol

from bot_car_number.application.dto.stats import StatsDTO


class StatsGateway(Protocol):
    @abstractmethod
    async def add_search_try(self, stats: StatsDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_search_count(self, user_id: int) -> int:
        raise NotADirectoryError
