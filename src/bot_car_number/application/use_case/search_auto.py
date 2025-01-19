from bot_car_number.application.dto.stats import StatsDTO
from bot_car_number.application.gateways.auto import AutoGateway
from bot_car_number.application.gateways.stats import StatsGateway
from bot_car_number.application.gateways.user import UserGateway
from bot_car_number.config_loader import SEARCH_COUNT_LIMIT
from bot_car_number.domain.exceptions import AutoNumberValidationError
from bot_car_number.domain.value_objects import Auto
from bot_car_number.presentation.misc import msg


class GetAutoOwnerData:
    def __init__(
        self,
        auto_gateway: AutoGateway,
        user_gateway: UserGateway,
        stats_gateway: StatsGateway,
    ) -> None:
        self.auto_gateway = auto_gateway
        self.user_gateway = user_gateway
        self.stats_gateway = stats_gateway

    async def __call__(self, number: str, tg_id: int) -> tuple[str, bool]:
        try:
            auto = Auto(number=number, model=None)
        except AutoNumberValidationError:
            return msg.AUTO_FORMAT_ERR_MSG, False

        user = await self.user_gateway.get_user_by_telegram_id(tg_id=tg_id)
        search_count = await self.stats_gateway.get_search_count(
            user_id=user.id
        )
        if search_count >= SEARCH_COUNT_LIMIT:
            return msg.SEARCH_ACCESS_DENIED, True

        stats = StatsDTO(user_id=user.id, number=auto.number)
        await self.stats_gateway.add_search_try(stats=stats)

        auto_data = await self.auto_gateway.get_auto_by_number(
            number=auto.number
        )
        if not auto_data:
            return msg.AUTO_NOT_EXIST_MSG, False

        if user.id == auto_data.user_id:
            return msg.OWNER_YOUR_MSG, True

        owner = await self.user_gateway.get_user(user_id=auto_data.user_id)
        return msg.OWNER_MSG.format(owner.phone), True
