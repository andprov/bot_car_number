from app.dao.stats import StatsDAO


class SearchService:
    """..."""

    @classmethod
    async def add_search_try(cls, dao: StatsDAO, user_id: int):
        """Добавить запись о поиске."""
        await dao.add(user_id=user_id)
