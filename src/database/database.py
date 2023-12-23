from typing import Annotated

from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import async_link

engine = create_async_engine(async_link, echo=True)

session = sessionmaker(engine)

str_256 = Annotated[str, String(256)]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }
