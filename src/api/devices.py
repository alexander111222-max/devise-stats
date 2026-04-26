from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.devices import DeviceAddSchema
from src.services.devices import DeviceService
from src.utils.exceptions import DeviceCreationException, DeviceNotFoundException

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post(
    "/",
    summary="Добавить устройство",
    description="Регистрирует новое устройство и привязывает его к пользователю.",
)
async def add_device(data: DeviceAddSchema, db: DBDep):
    try:
        device = await DeviceService(db).add_device(data)
        return device

    except DeviceCreationException:
        raise HTTPException(status_code=400, detail="Ошибка при создании устройства")


@router.get(
    "/{device_id}",
    summary="Получить устройство",
    description="Возвращает информацию об устройстве по его идентификатору.",
)
async def get_device(device_id: int, db: DBDep):
    try:
        device = await DeviceService(db).get_device(device_id)
        return device
    except DeviceNotFoundException:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
