from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.task import TaskRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.task_repository = TaskRepository(session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
