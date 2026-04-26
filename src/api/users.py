# src/api/users
from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.users import UserAddRequestSchema
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(data: UserAddRequestSchema, db: DBDep):
    user = await UserService(db).add_user(data)
    return user
