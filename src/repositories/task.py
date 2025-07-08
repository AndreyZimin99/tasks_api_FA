from typing import Generic, TypeVar
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import UUID


from src.models.base import Base
from src.models.models import Task

M = TypeVar('M', bound=Base)


class TaskRepository(Generic[M]):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_task(self, session: AsyncSession, task_data) -> Task:
        task = Task(**task_data)
        session.add(task)
        await session.flush()
        return task

    async def get_task(self, session: AsyncSession, task_id: UUID) -> Task:
        result = await session.execute(select(Task).options(
            selectinload(Task.watchers),
            selectinload(Task.executors)
        ).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail='Задача не найдена')
        return task

    async def get_all_tasks(self, session: AsyncSession):
        result = await session.execute(select(Task).options(
            selectinload(Task.watchers),
            selectinload(Task.executors))
        )
        return result.scalars().all()

    async def delete_task(self, session: AsyncSession, task_id: UUID) -> None:
        task = await self.get_task(session, task_id)
        if task:
            await session.delete(task)

    async def update_task(
        self,
        session: AsyncSession,
        task_id: UUID,
        task_data
    ) -> Task | None:
        task = await self.get_task(session, task_id)
        if task:
            for key, value in task_data.items():
                setattr(task, key, value)
        return task
