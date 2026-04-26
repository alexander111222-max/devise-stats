from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.users import UserAddRequestSchema
from src.services.users import UserService
from src.utils.exceptions import UserCreationException, UserAlreadyExistsException

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    summary="Создать пользователя",
    description="Регистрирует нового пользователя. Email должен быть уникальным.",
)
async def create_user(data: UserAddRequestSchema, db: DBDep):
    try:
        user = await UserService(db).add_user(data)
        return user

    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=409, detail="Пользователь с таким email уже существует"
        )

    except UserCreationException:
        raise HTTPException(status_code=400, detail="Ошибка при создании пользователя")
