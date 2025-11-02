from bot_car_number.application.config import MAX_REGISTRATIONS_COUNT
from bot_car_number.application.interfaces.registration import (
    RegistrationGateway,
)


class AddRegistrationCount:
    def __init__(self, registration_gateway: RegistrationGateway) -> None:
        self.registration_gateway = registration_gateway

    async def __call__(self, tg_id: int) -> bool:
        registration_count = (
            await self.registration_gateway.get_registrations_count(
                tg_id=tg_id
            )
        )

        if registration_count is None:
            await self.registration_gateway.add_registration(tg_id=tg_id)
            return True

        if registration_count > MAX_REGISTRATIONS_COUNT:
            return False

        await self.registration_gateway.increase_registrations_count(
            tg_id=tg_id
        )
        return True
