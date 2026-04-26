from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.measurements import MeasurementAddRequestSchema
from src.services.measurements import MeasurementService
from src.utils.exceptions import MeasurementCreationException

router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.post(
    "/{device_id}",
    summary="Записать измерение",
    description="Принимает измерение в формате {x, y, z} и сохраняет его для указанного устройства.",
)
async def add_measurement(device_id: int, data: MeasurementAddRequestSchema, db: DBDep):
    try:
        measurement = await MeasurementService(db).add_measurement(device_id, data)
        return measurement
    except MeasurementCreationException:
        raise HTTPException(status_code=400, detail="Ошибка при сохранении измерения")
