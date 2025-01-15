from bot_car_number.application.gateways.registration import (
    RegistrationGateway,
)
from bot_car_number.config_loader import MAX_REGISTRATIONS_COUNT


class AddRegistrationCount:
    def __init__(self, gateway: RegistrationGateway) -> None:
        self.gateway = gateway

    async def __call__(self, tg_id: int) -> bool:
        registration_count = await self.gateway.get_registrations_count(
            tg_id=tg_id
        )

        if registration_count > MAX_REGISTRATIONS_COUNT:
            return False

        if registration_count == 0:
            await self.gateway.add_registration(tg_id=tg_id)
            return True

        await self.gateway.increase_registrations_count(tg_id=tg_id)
        return True
