import logging

from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.domain.exceptions import AutoNumberValidationError
from bot_car_number.domain.value_objects import Auto
from bot_car_number.presentation.misc import msg

logger = logging.getLogger(__name__)


class AddAutoNumber:
    def __init__(self, gateway: AutoGateway) -> None:
        self.gateway = gateway

    async def __call__(self, number: str) -> tuple[str | None, None | str]:
        try:
            auto = Auto(number=number, model=None)
        except AutoNumberValidationError as err:
            logger.warning(err.message)
            return None, msg.AUTO_FORMAT_ERR_MSG

        if await self.gateway.get_auto_by_number(number=auto.number):
            return None, msg.AUTO_EXIST_MSG

        return auto.number, None
