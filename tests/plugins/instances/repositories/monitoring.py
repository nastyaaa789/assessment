import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from assessment_service.infrastructure.database.repositories.monitoring import (
    PGMonitoringRepository,
)


@pytest.fixture
def pg_monitoring_repository(session: AsyncSession) -> PGMonitoringRepository:
    return PGMonitoringRepository(session=session)
