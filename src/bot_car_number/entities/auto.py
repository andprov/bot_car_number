from dataclasses import dataclass


@dataclass
class Auto:
    id: int | None
    number: str
    model: str
    user_id: int
