from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase

TEST_TASK_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 'First Test Task',
            'description': 'First Test Description',
            'status': 'done',
            'author_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'assignee_id': None,
            'column_id': None,
            'sprint_id': None,
            'board_id': None,
            'group_id': None,
            'watchers': [],
            'executors': [],
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'title': 'First Test Task',
            'description': 'First Test Description',
            'status': 'done',
            'author_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'assignee_id': None,
            'column_id': None,
            'sprint_id': None,
            'board_id': None,
            'group_id': None,
            'watchers': [],
            'executors': [],
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/',
        headers={},
        data={
            'title': 'First Test Task',
            'description': 'First Test Description',
            'status': 'waiting',
            'author_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'assignee_id': None,
            'column_id': None,
            'sprint_id': None,
            'board_id': None,
            'group_id': None,
            'watchers': [],
            'executors': [],
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Unexpected status',
    ),
]

TEST_TASK_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/b04e55bd-8431-4edd-8eb4-632099c0ea65',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
            'title': 'First Test Task',
            'description': 'First Test Description',
            'status': 'done',
            'author_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'assignee_id': None,
            'column_id': None,
            'sprint_id': None,
            'board_id': None,
            'group_id': None,
            'watchers': [],
            'executors': [],
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/1',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid task id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent task',
    ),
]
