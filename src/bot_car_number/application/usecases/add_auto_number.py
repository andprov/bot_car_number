import logging

from bot_car_number.application.exceptions import AutoAlreadyExistsError
from bot_car_number.application.interfaces.auto import AutoGateway
from bot_car_number.value_objects.auto_number import AutoNumber

logger = logging.getLogger(__name__)


class AddAutoNumber:
    def __init__(self, auto_gateway: AutoGateway) -> None:
        self.auto_gateway = auto_gateway

    async def __call__(self, number: str) -> str:
        auto_number = AutoNumber(value=number)
        if await self.auto_gateway.get_auto_by_number(number=auto_number.value):
            logger.warning(
                f"[UC] Auto already exists | [auto: {auto_number.value}]"
            )
            raise AutoAlreadyExistsError()

        return auto_number.value
