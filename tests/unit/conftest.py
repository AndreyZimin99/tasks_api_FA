from datetime import datetime
from collections.abc import Sequence
from copy import deepcopy

import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Task, User
from src.utils.custom_types import AsyncFunc
from tests import fixtures
from tests.utils import bulk_save_models


@pytest_asyncio.fixture
async def setup_tasks(transaction_session: AsyncSession, tasks: tuple[dict]) -> None:
    """Creates tasks that will only exist within the session."""
    await bulk_save_models(transaction_session, Task, tasks)


@pytest_asyncio.fixture
async def setup_users(setup_tasks: None, transaction_session: AsyncSession, users: tuple[dict]) -> None:
    """Creates users that will only exist within the session."""
    await bulk_save_models(transaction_session, User, users)


@pytest_asyncio.fixture
def get_tasks(transaction_session: AsyncSession) -> AsyncFunc:
    """Returns users existing within the session."""
    async def _get_tasks() -> Sequence[Task]:
        res: Result = await transaction_session.execute(select(Task))
        return res.scalars().all()
    return _get_tasks


@pytest_asyncio.fixture
def get_users(transaction_session: AsyncSession) -> AsyncFunc:
    """Returns users existing within the session."""
    async def _get_users() -> Sequence[User]:
        res: Result = await transaction_session.execute(select(User))
        return res.scalars().all()
    return _get_users


@pytest.fixture
def tasks() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.TASKS)


@pytest.fixture
def users() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.USERS)


@pytest.fixture
def first_user() -> dict:
    return deepcopy(fixtures.db_mocks.USERS[0])
