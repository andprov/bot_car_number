from dataclasses import dataclass


@dataclass
class Auto:
    id: int
    number: str
    model: str
    user_id: int
