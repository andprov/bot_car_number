from dataclasses import dataclass


@dataclass
class AutoDTO:
    id: int | None
    number: str
    model: str
    user_id: int
