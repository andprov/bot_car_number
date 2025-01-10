from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int | None
    tg_id: int
    first_name: str
    phone: str
    banned: bool
