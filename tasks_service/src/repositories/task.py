from pydantic import UUID4
from sqlalchemy import Sequence, delete, insert, select, update
from sqlalchemy.orm import selectinload
from typing import TYPE_CHECKING, Any

from src.models.models import Task, User, TaskExecutors, TaskWatchers
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

    # async def add_one_and_get_task(self, **kwargs: Any) -> Task:
    #     try:
    #         # Сначала извлекаем watchers и executors из kwargs
    #         watchers_ids = kwargs.pop('watchers', [])
    #         executors_ids = kwargs.pop('executors', [])

    #         # Создаем запрос для вставки задачи
    #         print(f'Данные: {kwargs}')
    #         query = insert(self._model).values(**kwargs).returning(self._model)
    #         print(f'Смотрим тут {query}')

    #         result = await self._session.execute(query)
    #         print('а тут?')
    #         obj = result.scalar_one()
    #         self._session.add(obj)

    #     except Exception as e:
    #         print(f'Ошибка: {e}')

    #     # Обработка связи "многие ко многим" для watchers
    #     if watchers_ids:
    #         for watcher_id in watchers_ids:
    #             watcher = await self._session.execute(select(User).where(User.id == watcher_id))
    #             watcher_obj = watcher.scalar_one_or_none()
    #             if watcher_obj:
    #                 obj.watchers.append(watcher_obj)

    #     # Обработка связи "многие ко многим" для executors
    #     if executors_ids:
    #         for executor_id in executors_ids:
    #             executor = await self._session.execute(select(User).where(User.id == executor_id))
    #             executor_obj = executor.scalar_one_or_none()
    #             if executor_obj:
    #                 obj.executors.append(executor_obj)

    #     return obj
    
    async def add_one_and_get_task(self, **kwargs: Any) -> Task:
        try:
            # Извлекаем watchers и executors из kwargs
            watchers_ids = kwargs.pop('watchers', [])
            executors_ids = kwargs.pop('executors', [])

            # Создаем запрос для вставки задачи
            query = insert(self._model).values(**kwargs).returning(self._model)
            
            result = await self._session.execute(query)
            obj = result.scalar_one()

            # Привязываем объект к сессии
            self._session.add(obj)

        except Exception as e:
            print(f'Ошибка: {e}')

        # Обработка связи "многие ко многим" для watchers
        if watchers_ids:
            for watcher_id in watchers_ids:
                watcher = await self._session.execute(select(User).where(User.id == watcher_id))
                watcher_obj = watcher.scalar_one_or_none()
                if watcher_obj:
                    obj.watchers.append(watcher_obj)

        # Обработка связи "многие ко многим" для executors
        if executors_ids:
            for executor_id in executors_ids:
                executor = await self._session.execute(select(User).where(User.id == executor_id))
                executor_obj = executor.scalar_one_or_none()
                if executor_obj:
                    obj.executors.append(executor_obj)

        # Сохраняем изменения в базе данных

        return obj

    # async def add_one_and_get_task(self, task_data: dict):
    #     # Извлечение основных данных задачи
    #     task_values = {
    #         'title': task_data['title'],
    #         'description': task_data['description'],
    #         'status': task_data['status'],
    #         'author_id': task_data['author_id'],
    #         'id': task_data['id'],
    #         'created_at': task_data['created_at'],
    #         'assignee_id': task_data['assignee_id'],
    #         'column_id': task_data['column_id'],
    #         'sprint_id': task_data['sprint_id'],
    #         'board_id': task_data['board_id'],
    #         'group_id': task_data['group_id'],
    #     }

    #     # Вставка задачи
    #     task_query = insert(self._model).values(**task_values).returning(self._model)
        
    #     try:
    #         result = await self._session.execute(task_query)
    #         new_task = result.fetchone()

    #         # Обработка watchers
    #         for watcher in task_data.get('watchers', []):
    #             watcher_values = {
    #                 'task_id': new_task.id,  # Предполагается, что у вас есть связь между задачей и наблюдателями
    #                 'id': watcher['id'],
    #                 'full_name': watcher['full_name'],
    #                 'email': watcher['email']
    #             }
    #             watcher_query = insert(TaskWatchers).values(**watcher_values)
    #             await self._session.execute(watcher_query)

    #         # Обработка executors
    #         for executor in task_data.get('executors', []):
    #             executor_values = {
    #                 'task_id': new_task.id,  # Предполагается, что у вас есть связь между задачей и исполнителями
    #                 'id': executor['id'],
    #                 'full_name': executor['full_name'],
    #                 'email': executor['email']
    #             }
    #             executor_query = insert(TaskExecutors).values(**executor_values)
    #             await self._session.execute(executor_query)
    #         return new_task  # Возвращаем созданную задачу

    #     except Exception as e:
    #         print(f"Ошибка выполнения запроса: {e}")