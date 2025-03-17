from assessment_service.common.entities.monitoring import Monitoring
from assessment_service.domains.monitoring.repositories.monitoring import (
    IMonitoringRepository,
)


class MonitoringService:
    __db_monitoring_repository: IMonitoringRepository

    def __init__(
        self,
        db_monitoring_repository: IMonitoringRepository,
    ) -> None:
        self.__db_monitoring_repository = db_monitoring_repository

    async def monitoring(self) -> Monitoring:
        db_check = await self.__db_monitoring_repository.check_connection()
        return Monitoring(db=db_check)
