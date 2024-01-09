from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from src.database.models import WorkType, ExperienceFilter, Employment, Sex
from src.database.queries.orm import AsyncORM

router = APIRouter()


@router.get("/workers")
@cache(expire=30)
async def getting_workers_from_db():
    workers = await AsyncORM.convert_workers_to_dto()
    return workers


@router.post("/create_worker")
async def create_worker(first_name: str, last_name: str, sex: Sex):
    worker = await AsyncORM.insert_worker(first_name, last_name, sex)
    return worker


@router.get("/resumes_filtration")
@cache(expire=30)
async def getting_resumes_due_filters(specialization: str = None, experience: ExperienceFilter = None,
                                      work_type: WorkType = None):
    workers = await AsyncORM.convert_workers_with_options_to_dto(specialization, experience, work_type)
    if len(workers) == 0:
        return JSONResponse(status_code=404, content={"message": "Error on the client-side"})
    return workers


@router.post("/create_resume")
async def creation_worker_resume(title: str, salary: int, specialization: str = None,
                                 employment: Employment = None,
                                 experience: int = None, work_type: WorkType = None):
    await AsyncORM.creation_resume_for_worker_post(title, salary, specialization, employment,
                                                   experience, work_type)
    return JSONResponse(status_code=201, content={"msg": "Created!"})


@router.post("/create_vacancy")
async def creation_vacancy(title: str, salary: int):
    await AsyncORM.creation_vacancy(title, salary)
    return JSONResponse(status_code=201, content={"msg": "Created!"})


@router.get("/vacancies")
@cache(expire=30)
async def select_available_vacancies():
    vacancies = await AsyncORM.select_vacancies()
    return vacancies


@router.get("/replied_vacancies")
@cache(expire=30)
async def select_replied_vacancies():
    rel_vacancies = await AsyncORM.select_resumes_with_all_relationships()
    return rel_vacancies
