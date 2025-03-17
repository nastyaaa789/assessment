import logging

from aiomisc import timeout
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from assessment_service.domains.monitoring.repositories.monitoring import (
    IMonitoringRepository,
)

log = logging.getLogger(__name__)


class PGMonitoringRepository(IMonitoringRepository):
    __session: AsyncSession

    def __init__(self, *, session: AsyncSession) -> None:
        self.__session = session

    async def check_connection(self) -> bool:
        try:
            return await self._check_connection()
        except (ConnectionError, TimeoutError, SQLAlchemyError) as e:
            log.warning("Can't connect to database: %s", e)
            return False

    @timeout(2)
    async def _check_connection(self) -> bool:
        await self.__session.execute(text("SELECT 1"))
        return True
