from bot_car_number.adapters.postgres.gateways.user import DatabaseUserGateway


#  TODO: fix
class UserService:
    @classmethod
    async def get_user_banned(
        cls, dao: DatabaseUserGateway, tg_id: int
    ) -> bool:
        user = await dao.get_user_by_telegram_id(tg_id=tg_id)
        if user:
            return user.banned
        return False
