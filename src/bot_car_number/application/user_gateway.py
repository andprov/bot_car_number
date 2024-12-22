from abc import abstractmethod
from typing import Protocol

from bot_car_number.entities.user import User


class UserGateway(Protocol):
    @abstractmethod
    async def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_telegram_id(self, tg_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def ban_user(self, tg_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, tg_id: int) -> None:
        raise NotImplementedError
