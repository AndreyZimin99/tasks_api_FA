from collections.abc import Awaitable, Callable
from typing import Any
from enum import Enum

AsyncFunc = Callable[..., Awaitable[Any]]


class Status(Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'
