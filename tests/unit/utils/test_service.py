from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.task import TaskResponse
from src.utils.custom_types import AsyncFunc
from tests.fixtures import FakeBaseService, testing_cases
from tests.utils import BaseTestCase, compare_dicts_and_db_models

if TYPE_CHECKING:
    from collections.abc import Sequence

    from src.models import Task


class TestBaseService:
    class _BaseService(FakeBaseService):
        _repo = 'user'

    def __get_service(self, session: AsyncSession) -> FakeBaseService:
        return self._BaseService(session)

    # @pytest.mark.usefixtures('setup_companies')
    # async def test_add_one(
    #     self,
    #     transaction_session: AsyncSession,
    #     first_user: dict,
    #     get_users: AsyncFunc,
    # ) -> None:
    #     service = self.__get_service(transaction_session)
    #     await service.add_one(**first_user)

    #     users_in_db: Sequence[UserModel] = await get_users()
    #     assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    # @pytest.mark.usefixtures('setup_companies')
    # async def test_add_one_and_get_id(
    #     self,
    #     transaction_session: AsyncSession,
    #     first_user: dict,
    #     get_users: AsyncFunc,
    # ) -> None:
    #     service = self.__get_service(transaction_session)
    #     user_id = await service.add_one_and_get_id(**first_user)
    #     assert user_id == first_user.get('id')

    #     users_in_db: Sequence[UserModel] = await get_users()
    #     assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_tasks')
    async def test_add_one_and_get_obj(
        self,
        transaction_session: AsyncSession,
        first_task: dict,
        get_tasks: AsyncFunc,
    ) -> None:
        service = self.__get_service(transaction_session)
        task = await service.add_one_and_get_obj(**first_task)
        assert task.id == first_task.get('id')

        tasks_in_db: Sequence[Task] = await get_tasks()
        assert compare_dicts_and_db_models(tasks_in_db, [first_task], TaskResponse)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS)
    async def test_get_by_filter_one_or_none(
        self,
        case: BaseTestCase,
        transaction_session: AsyncSession,
    ) -> None:
        service = self.__get_service(transaction_session)
        with case.expected_error:
            task_in_db: Task | None = await service.get_by_filter_one_or_none(**case.data)
            result = None if not task_in_db else task_in_db.to_schema()
            assert result == case.expected_data

    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS)
    # async def test_get_by_filter_all(
    #     self,
    #     case: BaseTestCase,
    #     transaction_session: AsyncSession,
    # ) -> None:
    #     service = self.__get_service(transaction_session)
    #     with case.expected_error:
    #         users_in_db: Sequence[UserModel] = await service.get_by_filter_all(**case.data)
    #         assert compare_dicts_and_db_models(users_in_db, case.expected_data, UserDB)

    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS)
    # async def test_update_one_by_id(
    #     self,
    #     case: BaseTestCase,
    #     transaction_session: AsyncSession,
    # ) -> None:
    #     service = self.__get_service(transaction_session)
    #     with case.expected_error:
    #         updated_user: UserModel | None = await service.update_one_by_id(case.data.pop('_id'), **case.data)
    #         assert updated_user.to_schema() == case.expected_data

    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS)
    # async def test_delete_by_filter(
    #     self,
    #     case: BaseTestCase,
    #     transaction_session: AsyncSession,
    #     get_users: AsyncFunc,
    # ) -> None:
    #     service = self.__get_service(transaction_session)
    #     with case.expected_error:
    #         await service.delete_by_filter(**case.data)
    #         users_in_db: Sequence[UserModel] = await get_users()
    #         assert compare_dicts_and_db_models(users_in_db, case.expected_data, UserDB)

    # @pytest.mark.usefixtures('setup_users')
    # async def test_delete_all(
    #     self,
    #     transaction_session: AsyncSession,
    #     get_users: AsyncFunc,
    # ) -> None:
    #     service = self.__get_service(transaction_session)
    #     await service.delete_all()
    #     users_in_db: Sequence[UserModel] = await get_users()
    #     assert users_in_db == []
