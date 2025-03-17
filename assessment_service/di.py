from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from assessment_service.args import Parser
from assessment_service.domains.monitoring.services.monitoring import MonitoringService
from assessment_service.infrastructure.database.gateway import DatabaseGateway
from assessment_service.infrastructure.database.repositories.monitoring import (
    PGMonitoringRepository,
)
from assessment_service.infrastructure.database.uow import SQLAlchemyUnitOfWork
from assessment_service.infrastructure.database.utils import (
    create_engine,
    create_session_factory,
)


class MainProvider(Provider):
    _parser: Parser

    def __init__(self, parser: Parser):
        super().__init__()
        self._parser = parser

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        engine = create_engine(
            url=self._parser.database.url,
            debug=self._parser.debug,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_factory(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(session=session_factory())

    @provide(scope=Scope.REQUEST)
    async def database_gateway(
        self,
        uow: SQLAlchemyUnitOfWork,
    ) -> AsyncIterator[DatabaseGateway]:
        async with DatabaseGateway(uow) as gateway:
            yield gateway

    @provide(scope=Scope.REQUEST)
    def pg_monitoring_repository(
        self, gateway: DatabaseGateway
    ) -> PGMonitoringRepository:
        return gateway.monitoring()

    @provide(scope=Scope.REQUEST)
    def monitoring_service(
        self, pg_monitoring_repository: PGMonitoringRepository
    ) -> MonitoringService:
        return MonitoringService(db_monitoring_repository=pg_monitoring_repository)
