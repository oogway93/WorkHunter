import asyncio
import os
import sys

import aioredis
from fastapi import FastAPI, Depends
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_users import FastAPIUsers
from fastapi_cache.backends.redis import RedisBackend

from config import REDIS_PORT
from src.auth.database import User
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.database.queries.orm import AsyncORM
from src.api.api import api_router
from src.database.database import Base

sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI()

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
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(api_router)


@app.on_event(event_type="startup")
async def startup():
    redis = aioredis.from_url(
        f"redis://localhost:{REDIS_PORT}", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


async def main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_worker()
    await AsyncORM.insert_resumes()
    await AsyncORM.insert_vacancies()
    await AsyncORM.insert_vacancy_replies()


if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run("src.main:app", reload=True)
