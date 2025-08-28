from abc import abstractmethod
from typing import Protocol


class RegistrationGateway(Protocol):
    @abstractmethod
    async def add_registration(self, tg_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_registrations_count(self, tg_id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def increase_registrations_count(self, tg_id: int) -> None:
        raise NotImplementedError
