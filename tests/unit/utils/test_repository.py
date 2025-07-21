
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Task
from src.schemas.user import UserDB
from src.schemas.task import TaskCreateRequest, TaskResponse
from src.utils.custom_types import AsyncFunc
from src.utils.repository import SqlAlchemyRepository
from tests.fixtures import testing_cases
from tests.utils import BaseTestCase, compare_dicts_and_db_models

if TYPE_CHECKING:
    from collections.abc import Sequence


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        _model = Task

    def __get_sql_rep(self, session: AsyncSession) -> SqlAlchemyRepository:
        return self._SqlAlchemyRepository(session)

    # @pytest.mark.usefixtures('setup_companies')
    # async def test_add_one(
    #     self,
    #     transaction_session: AsyncSession,
    #     first_user: dict,
    #     get_users: AsyncFunc,
    # ) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #     await sql_rep.add_one(**first_user)
    #     await transaction_session.flush()

    #     users_in_db: Sequence[UserModel] = await get_users()
    #     assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_tasks')
    async def test_add_one_and_get_obj(
        self,
        transaction_session: AsyncSession,
        first_task: dict,
        get_tasks: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        task = await sql_rep.add_one_and_get_obj(**first_task)
        assert task.id == first_task.get('id')
        await transaction_session.flush()

        tasks_in_db: Sequence[Task] = await get_tasks()
        assert compare_dicts_and_db_models(tasks_in_db, [first_task], TaskCreateRequest)

    @pytest.mark.usefixtures('setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE_PARAMS)
    async def test_get_by_filter_one_or_none(
        self,
        case: BaseTestCase,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            task_in_db: Task | None = await sql_rep.get_by_filter_one_or_none(**case.data)  # вероятно с ф-цией разобр
            result = None if not task_in_db else task_in_db.to_schema()
            assert result == case.expected_data

    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL_PARAMS)
    # async def test_get_by_filter_all(
    #     self,
    #     case: BaseTestCase,
    #     transaction_session: AsyncSession,
    # ) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #     with case.expected_error:
    #         tasks_in_db: Sequence[Task] = await sql_rep.get_by_filter_all(**case.data)  # вероятно с ф-цией разобр
    #         assert compare_dicts_and_db_models(tasks_in_db, case.expected_data, Task)

    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID_PARAMS)
    # async def test_update_one_by_id(
    #     self,
    #     case: BaseTestCase,
    #     transaction_session: AsyncSession,
    # ) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #     with case.expected_error:
    #         updated_user: UserModel | None = await sql_rep.update_one_by_id(case.data.pop('_id'), **case.data)
    #         assert updated_user.to_schema() == case.expected_data

    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY_PARAMS)
    # async def test_delete_by_filter(
    #     self,
    #     case: BaseTestCase,
    #     transaction_session: AsyncSession,
    #     get_users: AsyncFunc,
    # ) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #     with case.expected_error:
    #         await sql_rep.delete_by_filter(**case.data)
    #         await transaction_session.flush()
    #         users_in_db: Sequence[UserModel] = await get_users()
    #         assert compare_dicts_and_db_models(users_in_db, case.expected_data, UserDB)
