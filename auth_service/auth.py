from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.token import TokenInfo
from schemas.user import CreateUser, UserSchema
import utils as auth_utils
from view import create_user, get_user_by_email, get_current_token_payload

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


@router.get('user/info')
async def auth_user_check_self_info(
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload)
) -> UserSchema:
    email: str | None = payload.get('sub')
    user = await get_user_by_email(db, email)
    if user:
        count = await auth_utils.get_task_count(user.id)
        return {
            'User': user,
            'task_count': count
            }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User not found',
    )
