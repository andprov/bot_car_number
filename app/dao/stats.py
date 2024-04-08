from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.db.models import Stats


class StatsDAO(BaseDAO[Stats]):
    """..."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Stats, session)
