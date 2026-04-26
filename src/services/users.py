from src.schemas.users import UserAddRequestSchema, UserAddSchema
from src.services.auth import AuthService
from src.services.base import BaseService


class UserService(BaseService):

    def __init__(self, db):
        super().__init__(db)

    async def add_user(self, data: UserAddRequestSchema):
        hashed_password = AuthService().get_password_hash(data.password)
        payload = data.model_dump(exclude={"password"})
        new_user = UserAddSchema(**payload, hashed_password=hashed_password)
        added_user = await self._db.users.add_one(new_user)
        await self._db.commit()

        return added_user

