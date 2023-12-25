from datetime import datetime

from pydantic import BaseModel

from src.database.models import Sex, Employment, WorkType


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
    work_type: WorkType


class ResumeDTO(ResumeAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class ResumeRelDTO(ResumeDTO):
    worker: "WorkerDTO"


class WorkerRelDTO(WorkerDTO):
    resume: list["ResumeDTO"]

