from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr, UUID4


class CreateUser(BaseModel):

    email: EmailStr
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: UUID4
    email: EmailStr
