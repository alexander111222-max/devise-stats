import logging

from src.schemas.devices import DeviceAddSchema
from src.services.base import BaseService
from src.utils.exceptions import (
    ObjectNotFoundException,
    DeviceCreationException,
    DeviceNotFoundException,
)


class DeviceService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    async def add_device(self, data: DeviceAddSchema):
        try:
            device = await self._db.devices.add_one(data)
            await self._db.commit()
            return device
        except ObjectNotFoundException:
            logging.error(f"Ошибка при создании устройства: {data.name}")
            raise DeviceCreationException

    async def get_device(self, device_id: int):

        device = await self._db.devices.get_one_or_none(device_id)
        if not device:
            logging.warning(f"Устройство id={device_id} не найдено")
            raise DeviceNotFoundException
        return device
