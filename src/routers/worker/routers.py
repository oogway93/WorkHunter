from fastapi import APIRouter

from src.database.queries.orm import AsyncORM

router = APIRouter()


@router.get("/workers")
async def getting_workers_from_db():
    workers = await AsyncORM.convert_workers_to_dto()
    return workers


@router.get("/resumes_filtration")
async def getting_resumes_due_filters(specialization: str = None, experience: str = None):
    workers = await AsyncORM.convert_workers_with_options_to_dto(specialization, experience)
    return workers
