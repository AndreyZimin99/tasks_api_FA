from collections.abc import AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_size=50,
    max_overflow=100,
    connect_args={
        'prepared_statement_name_func': lambda:  f'__asyncpg_{uuid4()}__',
    },
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as conn:
        yield conn


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session