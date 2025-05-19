import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

MAX_AUTO_NAME_LEN = 50


@dataclass
class AutoModelValidationError(ValueError):
    message: str = "Auto Model Validation Error"


@dataclass(frozen=True)
class AutoModel:
    value: str

    def __post_init__(self) -> None:
        if self.value and len(self.value) > MAX_AUTO_NAME_LEN:
            logger.warning(
                f"[VO] Auto Model Validation Error | [{self.value}]"
            )
            raise AutoModelValidationError()
