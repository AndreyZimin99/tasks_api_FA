import uvicorn
from fastapi import FastAPI

from auth_service.auth import router as jwt_router


auth = FastAPI()
auth.include_router(jwt_router)


if __name__ == '__main__':
    uvicorn.run('auth_service.main:auth', reload=True)
