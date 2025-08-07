from uuid import uuid4
from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, Text, text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base, str_100, str_120, str_255
from src.utils.custom_types import Status
from src.schemas.task import TaskResponse

uuidpk = Annotated[
    uuid4,
    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
]
created_at_user = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]
created_at_user_task = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"), index=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuidpk]
    watching_tasks: Mapped[list['Task']] = relationship(
        back_populates='watchers',
        secondary='task_watchers',
    )
    executioning_tasks: Mapped[list['Task']] = relationship(
        back_populates='executors',
        secondary='task_executors',
    )


# class User(Base):
#     __tablename__ = 'users'

#     id: Mapped[uuidpk]
#     full_name: Mapped[str_100]
#     email: Mapped[str_120] = mapped_column(unique=True)
#     created_at: Mapped[created_at_user]
#     watching_tasks: Mapped[list['Task']] = relationship(
#         back_populates='watchers',
#         secondary='task_watchers',
#     )
#     executioning_tasks: Mapped[list['Task']] = relationship(
#         back_populates='executors',
#         secondary='task_executors',
#     )


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[uuidpk]
    title: Mapped[str_255]
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[Status]
    created_at: Mapped[created_at_user_task]
    author_id: Mapped[UUID] = mapped_column(ForeignKey(
        'users.id',
        ondelete='CASCADE'))
    assignee_id: Mapped[UUID | None] = mapped_column(ForeignKey(
        'users.id',
        ondelete='CASCADE'))
    column_id: Mapped[UUID | None] = mapped_column(ForeignKey(
        'columns.id',
        ondelete='CASCADE'))
    sprint_id: Mapped[UUID | None] = mapped_column(ForeignKey(
        'sprints.id',
        ondelete='CASCADE'))
    board_id: Mapped[UUID | None] = mapped_column(ForeignKey(
        'boards.id',
        ondelete='CASCADE'))
    group_id: Mapped[UUID | None] = mapped_column(ForeignKey(
        'groups.id',
        ondelete='CASCADE'))
    watchers: Mapped[list['User']] = relationship(
        back_populates='watching_tasks',
        secondary='task_watchers',
        lazy='subquery'
    )
    executors: Mapped[list['User']] = relationship(
        back_populates='executioning_tasks',
        secondary='task_executors',
        lazy='subquery'
    )

    def to_schema(self) -> TaskResponse:
        return TaskResponse(**self.__dict__)


class Board(Base):
    __tablename__ = 'boards'

    id: Mapped[uuidpk]
    name: Mapped[str_100] = mapped_column(unique=True)


class Column(Base):
    __tablename__ = 'columns'

    id: Mapped[uuidpk]
    name: Mapped[str_100]
    board_id: Mapped[UUID | None] = mapped_column(ForeignKey(
        'users.id',
        ondelete='CASCADE'))


class Sprint(Base):
    __tablename__ = 'sprints'

    id: Mapped[uuidpk]
    name: Mapped[str_100]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[uuidpk]
    name: Mapped[str_100]


class TaskWatchers(Base):
    __tablename__ = 'task_watchers'

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        primary_key=True
    )
    watcher_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )


class TaskExecutors(Base):
    __tablename__ = 'task_executors'

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        primary_key=True
    )
    executor_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
