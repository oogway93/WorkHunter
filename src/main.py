import asyncio
import os
import sys

from fastapi import FastAPI
import uvicorn

from src.database.queries.orm import AsyncORM
from src.routers.routers import router as MainRouter
from src.routers.worker.routers import router as WorkerRouter

sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI()

app.include_router(MainRouter)
app.include_router(WorkerRouter)


async def main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_worker()
    await AsyncORM.insert_resumes()
    await AsyncORM.select_worker_resumes()
    await AsyncORM.insert_vacancies()
    await AsyncORM.insert_vacancy_replies()
    await AsyncORM.select_vacancy_replies()
    await AsyncORM.convert_workers_to_dto()


if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run("src.main:app", reload=True)
