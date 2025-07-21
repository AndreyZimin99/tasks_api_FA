from pydantic import UUID4
from sqlalchemy import Sequence, delete, insert, select, update
from sqlalchemy.orm import selectinload
from typing import TYPE_CHECKING, Any

from src.models.models import Task, User
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy.engine import Result


class TaskRepository(SqlAlchemyRepository[Task]):
    _model = Task

    async def get_task(self, task_id: UUID4) -> Task:
        result = await self._session.execute(select(self._model).options(
            selectinload(self._model.watchers),
            selectinload(self._model.executors)
        ).where(self._model.id == task_id))
        task = result.scalar_one_or_none()
        return task

    async def get_all_tasks(self) -> Sequence[Task]:
        result = await self._session.execute(select(self._model).options(
            selectinload(self._model.watchers),
            selectinload(self._model.executors))
        )
        return result.scalars().all()

    # async def add_task(self, **kwargs: Any):
    #     query = insert(self._model).values(**kwargs).returning(self._model)
    #     obj: Result = await self._session.execute(query)
    #     return obj.scalar_one()

    