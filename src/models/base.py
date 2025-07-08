from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_100 = Annotated[str, 100]
str_120 = Annotated[str, 120]
str_255 = Annotated[str, 255]


class Base(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        str_100: String(100)
    }
    type_annotation_map = {
        str_120: String(120)
    }
    type_annotation_map = {
        str_255: String(255)
    }
