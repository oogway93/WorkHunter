from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from src.database.models import WorkType, ExperienceFilter, Employment
from src.database.queries.orm import AsyncORM

router = APIRouter()


@router.get("/workers")
async def getting_workers_from_db():
    workers = await AsyncORM.convert_workers_to_dto()
    return workers


@router.get("/resumes_filtration")
async def getting_resumes_due_filters(specialization: str = None, experience: ExperienceFilter = None,
                                      work_type: WorkType = None):
    workers = await AsyncORM.convert_workers_with_options_to_dto(specialization, experience, work_type)
    if len(workers) == 0:
        return JSONResponse(status_code=404, content={"message": "Error on the client-side"})
    return workers


@router.post("/create_resume")
async def creation_worker_resume(title: str, salary: int, specialization: str = None, employment: Employment = None,
                                 experience: int = None, work_type: WorkType = None):
    await AsyncORM.creation_resume_for_worker_post(title, salary, specialization, employment,
                                                   experience, work_type)
    return JSONResponse(status_code=201, content={"msg": "Created!"})


@router.post("/create_vacancy")
async def creation_vacancy(title: str, salary: int):
    await AsyncORM.add_vacancies_and_replies(title, salary)
    return JSONResponse(status_code=201, content={"msg": "Created!"})


@router.get("/select_vacancies")
async def select_avaible_vacancies():
    vacancies = await AsyncORM.select_vacancies()
    return vacancies


@router.get("/select_replied_vacancies")
async def selecr_replied_vacancies():
    vacancies = await AsyncORM.select_resumes_with_all_relationships()
    return vacancies
