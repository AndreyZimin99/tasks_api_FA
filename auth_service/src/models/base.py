from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_120 = Annotated[str, 120]


class Base(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        str_120: String(120)
    }
