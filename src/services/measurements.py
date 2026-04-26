import logging


from src.schemas.measurements import MeasurementAddRequestSchema, MeasurementAddSchema
from src.services.base import BaseService
from src.utils.exceptions import ObjectCreationException, MeasurementCreationException


class MeasurementService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    async def add_measurement(self, device_id: int, data: MeasurementAddRequestSchema):
        try:
            measurement = await self._db.measurements.add_one(
                MeasurementAddSchema(device_id=device_id, **data.model_dump())
            )
            await self._db.commit()
            return measurement
        except ObjectCreationException:
            logging.error(f"Ошибка при сохранении измерения для device_id={device_id}")
            raise MeasurementCreationException
