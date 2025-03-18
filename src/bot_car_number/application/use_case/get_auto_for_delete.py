import logging

from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.domain.exceptions import AutoNumberValidationError
from bot_car_number.domain.value_objects import Auto
from bot_car_number.presentation.misc import msg

logger = logging.getLogger(__name__)


class GetAutoForDelete:
    def __init__(
        self,
        auto_gateway: AutoGateway,
        user_gateway: UserGateway,
    ) -> None:
        self.auto_gateway = auto_gateway
        self.user_gateway = user_gateway

    async def __call__(
        self,
        number: str,
        tg_id: int,
    ) -> tuple[AutoDTO | None, None | str]:
        try:
            auto = Auto(number=number, model=None)
        except AutoNumberValidationError as err:
            logger.warning(err.message)
            return None, msg.AUTO_FORMAT_ERR_MSG

        auto_data = await self.auto_gateway.get_auto_by_number(
            number=auto.number
        )
        if not auto_data:
            return None, msg.AUTO_NOT_EXIST_MSG

        user = await self.user_gateway.get_user_by_telegram_id(tg_id=tg_id)
        if user.id != auto_data.user_id:
            return None, msg.AUTO_NOT_YOURS_MSG

        return auto_data, None
