import re
from dataclasses import dataclass

from bot_car_number.domain.exceptions import (
    AutoModelValidationError,
    AutoNumberValidationError,
)

MAX_AUTO_NAME_LEN = 50


@dataclass(frozen=True)
class Auto:
    number: str | None
    model: str | None

    def __post_init__(self) -> None:
        pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
        if self.number and not pattern.match(self.number):
            raise AutoNumberValidationError(
                message="The number format does not match the template"
            )

        if self.model and len(self.model) > MAX_AUTO_NAME_LEN:
            raise AutoModelValidationError(
                message=(
                    "The number of characters in the car model is greater "
                    "than the allowed"
                )
            )
