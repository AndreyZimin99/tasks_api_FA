import uvicorn
from fastapi import FastAPI

from auth import router as jwt_router
from utils import get_rabbit_connection


auth = FastAPI()
auth.include_router(jwt_router)

rabbit_connection = None


@auth.on_event("startup")
async def startup_event():
    await get_rabbit_connection()


@auth.on_event("shutdown")
async def shutdown_event():
    global rabbit_connection
    if rabbit_connection:
        await rabbit_connection.close()


if __name__ == '__main__':
    uvicorn.run('auth_service.main:auth', reload=True)
