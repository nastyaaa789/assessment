from fastapi import APIRouter

from assessment_service.presentors.rest.api.v1.monitoring.endpoint import (
    monitoring_router,
)

v1_router = APIRouter()
v1_router.include_router(monitoring_router)
