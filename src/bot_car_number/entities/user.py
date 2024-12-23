from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    tg_id: int
    first_name: str
    phone: str
    banned: bool
