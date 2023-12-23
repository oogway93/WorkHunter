from typing import Annotated

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import async_link, link

engine = create_engine(link, echo=True)
async_engine = create_async_engine(async_link, echo=True)

session = sessionmaker(engine)
async_session = sessionmaker(async_engine)

str_256 = Annotated[str, String(256)]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }
