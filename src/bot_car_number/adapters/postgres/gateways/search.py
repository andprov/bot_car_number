import logging
from datetime import timedelta

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_car_number.adapters.postgres.tables import (
    SearchAttempt as SearchAttemptDNModel,
)
from bot_car_number.application.config import TIME_LIMIT
from bot_car_number.application.dto.search import SearchAttemptDTO
from bot_car_number.application.interfaces.search import SearchAttemptGateway

logger = logging.getLogger(__name__)


class DatabaseSearchAttemptGateway(SearchAttemptGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.model = SearchAttemptDNModel
        self.session = session

    async def add_search_attempt(self, search_data: SearchAttemptDTO) -> None:
        stmt = insert(self.model).values(
            tg_id=search_data.tg_id,
            number=search_data.number,
        )
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info(f"[DB] Add search attempt | [tg_id: {search_data.tg_id}]")

    async def get_search_attempt_count(self, tg_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(
            self.model.tg_id == tg_id,
            self.model.date >= func.now() - timedelta(hours=TIME_LIMIT),
        )
        result = await self.session.execute(stmt)
        logger.info(f"[DB] Get search attempt count | [tg_id: {tg_id}]")
        return result.scalar_one()
