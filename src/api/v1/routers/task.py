from pydantic import UUID4

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from api.v1.services.task import TaskService


router = APIRouter(tags=['Task'])


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
)
async def create_task(
    task: TaskCreateRequest,
    service: TaskService = Depends(TaskService),
) -> TaskResponse:
    """Create task."""
    created_task: TaskResponse = await service.create_task(task)
    return created_task


@router.get(
    path='/{task_id}',
    status_code=HTTP_200_OK,
)
async def get_task(
    task_id: UUID4,
    service: TaskService = Depends(),
) -> TaskResponse:
    """Get task by ID."""
    task: TaskResponse | None = await service.get_task_by_id(task_id)
    return task


@router.patch(
    path='/{task_id}',
    status_code=HTTP_200_OK,
)
async def update_task(
    task_id: UUID4,
    task: TaskUpdateRequest,
    service: TaskService = Depends(),
) -> TaskResponse:
    """Update task."""
    updated_task: TaskResponse = await service.update_task(task_id, task)
    return updated_task


@router.delete(
    path='/{task_id}',
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: UUID4,
    service: TaskService = Depends(),
) -> None:
    """Delete task."""
    await service.delete_task(task_id)


@router.get(
    path='',
    status_code=HTTP_200_OK,
)
async def get_tasks(
    service: TaskService = Depends(),
) -> list[TaskResponse]:
    """Get tasks."""
    tasks = await service.get_tasks()
    return tasks
