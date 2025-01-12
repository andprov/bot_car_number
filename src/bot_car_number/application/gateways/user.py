from abc import abstractmethod
from typing import Protocol

from bot_car_number.application.dto.user import UserDTO


class UserGateway(Protocol):
    @abstractmethod
    async def add_user(self, user: UserDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: int) -> UserDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_telegram_id(self, tg_id: int) -> UserDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def block_user(self, tg_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, tg_id: int) -> None:
        raise NotImplementedError
