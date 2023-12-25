from fastapi import APIRouter

from src.database.queries.orm import AsyncORM

router = APIRouter()


@router.get("/workers")
async def getting_workers_from_db():
    workers = await AsyncORM.convert_workers_to_dto()
    return workers

