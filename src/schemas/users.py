from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr # для маппера , чтобы возвращать юзера

    model_config = ConfigDict(from_attributes=True)

class UserAddSchema(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str


class UserAddRequestSchema(BaseModel):
    name: str
    email: EmailStr
    password: str