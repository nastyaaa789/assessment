from types import TracebackType
from typing import Self

from assessment_service.infrastructure.database.repositories.monitoring import (
    PGMonitoringRepository,
)
from assessment_service.infrastructure.database.uow import (
    SQLAlchemyUnitOfWork,
)


class DatabaseGateway:
    def __init__(self, uow: SQLAlchemyUnitOfWork):
        self.__uow = uow

    async def __aenter__(self) -> Self:
        await self.__uow.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.__uow.__aexit__(exc_type, exc_val, exc_tb)

    def monitoring(self) -> PGMonitoringRepository:
        return PGMonitoringRepository(session=self.__uow.session)
