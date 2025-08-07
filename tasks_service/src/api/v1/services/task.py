from typing import TYPE_CHECKING

from pydantic import UUID4

from src.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from collections.abc import Sequence

    from models import Task


class TaskService(BaseService):
    _repo: str = 'task'

    @transaction_mode
    async def create_task(self, task: TaskCreateRequest) -> TaskResponse:
        """Create task."""
        created_task: Task = await self.uow.task.add_one_and_get_task(**task.model_dump())
        return created_task

    @transaction_mode
    async def get_task_by_id(self, task_id: UUID4) -> TaskResponse:
        """Get task by ID."""
        task: Task | None = await self.uow.task.get_task(task_id=task_id)
        self.check_existence(obj=task, details='Задача не найдена')
        return task.to_schema()

    @transaction_mode
    async def update_task(self, task_id: UUID4, task: TaskUpdateRequest) -> TaskResponse:
        """Update task by ID."""
        task: Task | None = await self.uow.task.update_one_by_id(obj_id=task_id, **task.model_dump())
        self.check_existence(obj=task, details='Задача не найдена')
        return task.to_schema()

    @transaction_mode
    async def delete_task(self, task_id: UUID4) -> None:
        """Delete task by ID."""
        await self.uow.task.delete_by_ids(id=task_id)

    @transaction_mode
    async def get_tasks(self, ) -> list[TaskResponse]:
        """Get users by filter."""
        tasks: Sequence[Task] = await self.uow.task.get_all_tasks()
        return [task.to_schema() for task in tasks]
