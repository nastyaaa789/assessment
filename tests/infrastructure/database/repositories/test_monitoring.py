from assessment_service.infrastructure.database.repositories.monitoring import (
    PGMonitoringRepository,
)


async def test_check_connection(pg_monitoring_repository: PGMonitoringRepository):
    assert await pg_monitoring_repository.check_connection()
