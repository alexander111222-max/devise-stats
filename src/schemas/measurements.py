from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeasurementAddRequestSchema(BaseModel):
    x: float
    y: float
    z: float


class MeasurementAddSchema(BaseModel):
    device_id: int
    x: float
    y: float
    z: float


class MeasurementSchema(BaseModel):
    id: int
    device_id: int
    x: float
    y: float
    z: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
