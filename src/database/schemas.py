from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.database.models import Employment
from src.database.models import Sex
from src.database.models import WorkType


class WorkerAddDTO(BaseModel):
    first_name: str
    last_name: str
    sex: Sex


class WorkerDTO(WorkerAddDTO):
    id: int


class ResumeAddDTO(BaseModel):
    title: str
    salary: int
    specialization: str
    employment: Employment
    experience: int
    work_type: WorkType


class ResumeDTO(ResumeAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class ResumeRelDTO(ResumeDTO):
    worker: "WorkerDTO"


class WorkerRelDTO(WorkerDTO):
    resume: list["ResumeDTO"]


class VacanciesAddDTO(BaseModel):
    title: str
    salary: int


class VacanciesDTO(VacanciesAddDTO):
    id: int


class VacanciesWithoutCompensationDTO(BaseModel):
    id: int
    title: str


class ResumesRelVacanciesRepliedDTO(ResumeDTO):
    worker: "WorkerDTO"
    vacancy_replied: List["VacanciesDTO"]


class ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO(ResumeDTO):
    worker: "WorkerDTO"
    vacancy_replied: List["VacanciesWithoutCompensationDTO"]
