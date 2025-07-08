from pydantic import UUID4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_helper import db_helper
from src.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from src.api.v1.services.task import TaskService
from src.utils.unit_of_work import UnitOfWork


router = APIRouter(tags=['Task'])


@router.post('/', response_model=TaskResponse)
async def create_task(
    task: TaskCreateRequest,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    uow = UnitOfWork(db)
    service = TaskService(uow.task_repository)
    created_task = await service.create_task(uow, task.model_dump())
    return created_task


@router.get('/{task_id}/', response_model=TaskResponse)
async def get_task(
    id: UUID4,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    uow = UnitOfWork(db)
    service = TaskService(uow.task_repository)
    task = await service.get_task(uow, id)
    if not task:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return task


@router.get('/', response_model=list[TaskResponse])
async def get_all_tasks(
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    uow = UnitOfWork(db)
    service = TaskService(uow.task_repository)
    tasks = await service.get_all_tasks(uow)
    return tasks


@router.delete('/{task_id}/')
async def delete_task(
    id: UUID4,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    uow = UnitOfWork(db)
    service = TaskService(uow.task_repository)
    await service.delete_task(uow, id)


@router.patch('/{task_id}/', response_model=TaskResponse)
async def update_task(
    id: UUID4,
    task_update: TaskUpdateRequest,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    uow = UnitOfWork(db)
    service = TaskService(uow.task_repository)
    updated_task = await service.update_task(
        uow,
        id,
        task_update.model_dump(exclude_unset=True)
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return updated_task
