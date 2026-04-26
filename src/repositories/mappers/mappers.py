from src.models.devices import DeviceOrm
from src.models.measurements import MeasurementsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.devices import DeviceSchema
from src.schemas.measurements import MeasurementSchema
from src.schemas.users import UserSchema


class UserDataMapper(DataMapper):
    schema = UserSchema
    model = UsersOrm


class DeviceDataMapper(DataMapper):
    schema = DeviceSchema
    model = DeviceOrm


class MeasurementDataMapper(DataMapper):
    schema = MeasurementSchema
    model = MeasurementsOrm
