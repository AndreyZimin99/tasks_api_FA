from uuid import UUID

TASKS = (
    {
        'id': UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
        'title': 'First Test Task',
        'description': 'First Test Description',
        'status': 'done',
        'author_id': UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
        'assignee_id': None,
        'column_id': None,
        'sprint_id': None,
        'board_id': None,
        'group_id': None,
        'watchers': [],
        'executors': [],
    },
    {
        'id': UUID('9aff97eb-8b16-47d8-8ddc-dcdadb286d61'),
        'title': 'Second Test Task',
        'description': 'Second Test Description',
        'status': 'todo',
        'author_id': UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
        'assignee_id': None,
        'column_id': None,
        'sprint_id': None,
        'board_id': None,
        'group_id': None,
        'watchers': [],
        'executors': [],
    },
)
