import asyncio
import os
import sys

from fastapi import FastAPI, Depends
import uvicorn
from fastapi_users import FastAPIUsers

from src.auth.database import User
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.database.queries.orm import AsyncORM
from src.api.api import api_router

sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI()
app.include_router(api_router)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user(active=True, verified=True)


async def main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_worker()
    await AsyncORM.insert_resumes()
    await AsyncORM.insert_vacancies()
    await AsyncORM.insert_vacancy_replies()


if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run("src.main:app", reload=True)
