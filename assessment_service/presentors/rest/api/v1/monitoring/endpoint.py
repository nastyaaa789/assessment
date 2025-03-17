from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from assessment_service.domains.monitoring.services.monitoring import MonitoringService
from assessment_service.presentors.rest.api.v1.monitoring.models import (
    MonitoringStatusResponse,
)

monitoring_router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
    route_class=DishkaRoute,
)


@monitoring_router.get("/status")
async def status(
    monitoring_service: FromDishka[MonitoringService],
) -> MonitoringStatusResponse:
    monitoring = await monitoring_service.monitoring()
    return MonitoringStatusResponse.model_validate(monitoring)
