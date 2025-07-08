from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth_service import utils as auth_utils
from auth_service.models.user import User
from auth_service.schemas.user import CreateUser


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: CreateUser):
    db_user = User(
        email=user.email,
        hashed_password=auth_utils.hash_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
