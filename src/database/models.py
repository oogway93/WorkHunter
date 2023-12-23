import enum
from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]


class Sex(enum.Enum):
    male = "male"
    female = "male"


class Worker(Base):
    __tablename__ = 'worker'

    id: Mapped[intpk]
    first_name: Mapped[str_256]
    last_name: Mapped[str_256]
    sex = Mapped[Sex]
