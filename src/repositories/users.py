from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, UsersOrm)

    mapper = UserDataMapper
