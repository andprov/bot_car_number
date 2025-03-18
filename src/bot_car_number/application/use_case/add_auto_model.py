import logging

from bot_car_number.domain.exceptions import AutoModelValidationError
from bot_car_number.domain.value_objects import Auto
from bot_car_number.presentation.misc import msg

logger = logging.getLogger(__name__)


class AddAutoModel:
    async def __call__(self, model: str) -> tuple[str | None, None | str]:
        try:
            auto = Auto(number=None, model=model)
            return auto.model, None
        except AutoModelValidationError as err:
            logger.warning(err.message)
            return None, msg.AUTO_FORMAT_ERR_MSG
