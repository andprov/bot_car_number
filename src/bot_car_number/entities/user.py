from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    first_name: str
    phone: str
    banned: bool
    id: int | None = None
