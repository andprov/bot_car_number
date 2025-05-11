import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class AutoNumberValidationError(ValueError):
    message: str = "Auto Number Validation Error"


@dataclass(frozen=True)
class AutoNumber:
    value: str = field(init=False)

    def __init__(self, value: str) -> None:
        pattern = re.compile(r"^[А-Я]\d{3}[А-Я]{2}\d{2,3}$", re.UNICODE)
        normalized_value = value.upper()
        if not pattern.match(normalized_value):
            logger.warning(f"[VO] Auto Number Validation Error | [{value}]")
            raise AutoNumberValidationError()
        object.__setattr__(self, "value", normalized_value)
