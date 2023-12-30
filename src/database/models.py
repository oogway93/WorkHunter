import enum
from datetime import datetime
from typing import Annotated, List, Optional

from sqlalchemy import MetaData, text, ForeignKey, Index, CheckConstraint, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.utcnow,
)]

metadata_obj = MetaData()


class Sex(enum.Enum):
    male = "male"
    female = "female"


class Worker(Base):
    __tablename__ = 'worker'

    id: Mapped[intpk]
    first_name: Mapped[str_256]
    last_name: Mapped[str_256]
    sex: Mapped[Sex]

    resume: Mapped[List["Resume"]] = relationship(back_populates="worker")


class Employment(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    project_work = "project_work"


class WorkType(enum.Enum):
    remote = "remote"
    office = "office"
    combined = "combined"


class ExperienceFilter(enum.Enum):
    no_experience = "no experience"
    from_1_to_3 = "from 1 to 3 years"
    from_3_to_6 = "from 3 to 6 years"
    gt_6 = "greater 6 years"


class Resume(Base):
    __tablename__ = 'resume'

    id: Mapped[intpk]
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id"))
    title: Mapped[str_256]
    salary: Mapped[Optional[int]]
    specialization: Mapped[str_256]
    employment: Mapped[Employment]
    experience: Mapped[int]
    work_type: Mapped[WorkType]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped["Worker"] = relationship(back_populates="resume")

    vacancy_replied: Mapped[list["Vacancy"]] = relationship(
        back_populates="resume_replied",
        secondary="vacancy_reply",
    )

    repr_cols = ("salary",)

    _table_args__ = (
        Index("title_index", "title"),
        CheckConstraint("salary > 0", name="check_salary_positive"),
    )


class Vacancy(Base):
    __tablename__ = 'vacancy'

    id: Mapped[intpk]
    title: Mapped[str_256]
    salary: Mapped[Optional[int]]

    resume_replied: Mapped[list["Resume"]] = relationship(
        back_populates="vacancy_replied",
        secondary="vacancy_reply",
    )


class VacancyReply(Base):
    __tablename__ = 'vacancy_reply'

    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id", ondelete="CASCADE"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id", ondelete="CASCADE"), primary_key=True)
    cover_letter: Mapped[Optional[str]]
