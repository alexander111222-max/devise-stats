from pydantic import BaseModel, ConfigDict


class DeviceAddSchema(BaseModel):
    name: str
    user_id: int


class DeviceSchema(BaseModel):
    id: int
    name: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)
