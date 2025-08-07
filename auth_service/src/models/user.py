from uuid import uuid4
from typing import Annotated

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base, str_120

uuidpk = Annotated[
    uuid4,
    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuidpk]
    email: Mapped[str_120] = mapped_column(unique=True)
    hashed_password: Mapped[str]
