from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.schemas.token import TokenInfo
from auth_service.schemas.user import CreateUser, UserSchema
from auth_service import utils as auth_utils
from auth_service.view import create_user, get_user_by_email

from .database import db_helper


router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.post('/register/', response_model=UserSchema)
async def register(
    user: CreateUser,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь с данной почтой уже зарегистрирован'
            )
    return await create_user(db=db, user=user)


@router.post('/login/', response_model=TokenInfo)
async def login(
    form_data: CreateUser = Depends(),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await get_user_by_email(db, form_data.email)
    if (
        not user or
        not auth_utils.verify_password(
            form_data.password,
            user.hashed_password)
    ):
        raise HTTPException(status_code=400,
                            detail='Неверные почта или пароль')
    jwt_payload = {
        'sub': user.email,
        'id': str(user.id)
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        token=token,
        token_type='Bearer'
    )
