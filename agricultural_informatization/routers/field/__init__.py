from fastapi import APIRouter

from .fertilization import router as fertilization_router
from .sensor_data import router as sensor_data_router


router = APIRouter()

router.include_router(fertilization_router, prefix="/fertilization")
router.include_router(sensor_data_router, prefix="/sensor_data")


__all__ = [
    "router"
]