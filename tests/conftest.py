"""Contains helper fixtures for setup tests infrastructure."""

import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import AsyncClient
from sqlalchemy import Result, sql
from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.config import settings
from src.main import app
from src.models import Base
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures import FakeUnitOfWork

from sqlalchemy.exc import SQLAlchemyError



@pytest.fixture(scope='session')
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    """Returns a new event_loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def check_active_connections(connection, db_name):
    query = text(f"SELECT COUNT(*) FROM pg_stat_activity WHERE datname = '{db_name}'")
    result = await connection.execute(query)
    count = result.scalar()
    return count > 0


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_db(event_loop: None) -> None:
    assert settings.MODE == 'TEST'

    sqlalchemy_database_url = (
        f'postgresql+asyncpg://{settings.POSTGRES_USER}:'
        f'{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:'
        f'{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
    )
    nodb_engine = create_async_engine(
        sqlalchemy_database_url,
        echo=False,
        future=True,
    )

    async with nodb_engine.connect() as db:
        db_exists_query = text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        try:
            db_exists = await db.execute(db_exists_query)
            db_exists = db_exists.fetchone() is not None
            autocommit_engine = nodb_engine.execution_options(isolation_level='AUTOCOMMIT')
            async with autocommit_engine.connect() as connection:
                if not db_exists:
                    db_create_query = text(f'CREATE DATABASE {settings.POSTGRES_DB}')
                    await connection.execute(db_create_query)
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise

    yield

    autocommit_engine = nodb_engine.execution_options(isolation_level='AUTOCOMMIT')

    await nodb_engine.dispose()

    async with autocommit_engine.connect() as connection:
        if not await check_active_connections(connection, settings.POSTGRES_DB):
            db_drop_query = text(f'DROP DATABASE IF EXISTS {settings.POSTGRES_DB} WITH (FORCE)')
            await connection.execute(db_drop_query)


@pytest_asyncio.fixture(scope='session')
async def db_engine(create_test_db: None) -> AsyncGenerator[AsyncEngine, None]:
    """Returns the test Engine."""
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    ).execution_options(compiled_cache=None)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_schemas(db_engine: AsyncEngine) -> None:
    """Creates schemas in the test database."""
    assert settings.MODE == 'TEST'

    schemas = (
        'schema_for_example',
    )

    async with db_engine.connect() as conn:
        for schema in schemas:
            # Проверяем существование схемы
            result = await conn.execute(text(f"""
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name = :schema_name
            """), {'schema_name': schema})
            exists = result.scalar()

            if not exists:
                await conn.execute(sqlalchemy.schema.CreateSchema(schema))
                await conn.commit()



@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(db_engine: AsyncEngine, setup_schemas: None) -> None:
    """Creates tables in the test database and insert needs data."""
    assert settings.MODE == 'TEST'

    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.drop_all)
        await db_conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def transaction_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Returns a connection to the database.
    Any changes made to the database will NOT be applied, only for the duration of the TestCase.
    """
    connection = await db_engine.connect()
    await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.rollback()
    await connection.close()


@pytest_asyncio.fixture
def fake_uow(transaction_session: AsyncSession) -> FakeUnitOfWork:
    """Returns the test UnitOfWork for a particular test."""
    _fake_uow = FakeUnitOfWork(transaction_session)
    yield _fake_uow


@pytest_asyncio.fixture
async def async_client(fake_uow: FakeUnitOfWork) -> AsyncGenerator[AsyncClient, None]:
    """Returns async test client."""
    app.dependency_overrides[UnitOfWork] = lambda: fake_uow
    async with AsyncClient(base_url='http://localhost:8000') as ac:
        yield ac
