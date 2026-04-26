#src/repositories/mappers/mappers.py
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.users import UserSchema


class UserDataMapper(DataMapper):
    schema = UserSchema
    model = UsersOrm

