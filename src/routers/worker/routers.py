from fastapi import APIRouter

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
        return "Нет работников по заданным фильтрам"
    return workers


@router.post("/create_resume")
async def creation_worker_resume(title: str, salary: int, specialization: str = None,
                                 employment: Employment = None,
                                 experience: int = None, work_type: WorkType = None):
    await AsyncORM.creation_resume_for_worker_post(title, salary, specialization, employment,
                                                   experience, work_type)
    return {"title": title, "salary": salary, "specialization": specialization, "employment": employment,
            "experience": experience}
