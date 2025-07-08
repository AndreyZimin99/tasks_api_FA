from src.repositories.task import TaskRepository
from src.utils.unit_of_work import UnitOfWork


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, uow: UnitOfWork, task_data):
        task = await self.repository.create_task(uow.session, task_data)
        await uow.commit()
        return task

    async def get_task(self, uow: UnitOfWork, task_id):
        return await self.repository.get_task(uow.session, task_id)

    async def get_all_tasks(self, uow: UnitOfWork):
        return await self.repository.get_all_tasks(uow.session)

    async def delete_task(self, uow: UnitOfWork, task_id):
        await self.repository.delete_task(uow.session, task_id)
        await uow.commit()

    async def update_task(self, uow: UnitOfWork, task_id, task_data):
        updated_task = await self.repository.update_task(
            uow.session,
            task_id,
            task_data
        )
        if updated_task:
            await uow.commit()
            return updated_task
        return None
