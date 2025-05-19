from abc import abstractmethod
from typing import Protocol

from bot_car_number.application.dto.search import SearchAttemptDTO


class SearchAttemptGateway(Protocol):
    @abstractmethod
    async def add_search_attempt(self, search_data: SearchAttemptDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_search_attempt_count(self, tg_id: int) -> int:
        raise NotImplementedError
