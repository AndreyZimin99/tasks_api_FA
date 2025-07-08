import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.v1.routers.task import router as task_router

app = FastAPI()
app.include_router(task_router, prefix='/tasks')


if __name__ == '__main__':
    uvicorn.run('src.main:app', reload=True)
