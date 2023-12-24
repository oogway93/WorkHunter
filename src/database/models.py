import enum
from datetime import datetime
from typing import Annotated, List

from sqlalchemy import MetaData, text, ForeignKey
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


class Schedule(enum.Enum):
    full_time = "full_time"
    remote = "remote"


class Resume(Base):
    __tablename__ = 'resume'

    id: Mapped[intpk]
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id"))
    title: Mapped[str_256]
    salary: Mapped[int]
    specialization: Mapped[str_256]
    employment: Mapped[Employment]
    experience: Mapped[str_256]
    schedule: Mapped[Schedule]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped["Worker"] = relationship(back_populates="resume")

    repr_cols = ("salary",)
