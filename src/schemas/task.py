from pydantic import BaseModel, ConfigDict, Field, field_validator, UUID4
from datetime import datetime
from typing import List

from src.utils.status import Status
from .user import UserDB


class TaskBase(BaseModel):
    title: str = Field(min_length=3)
    description: str
    status: Status
    author_id: UUID4

    @field_validator('description')
    def validate_description(cls, value):
        if value and not all(
            c.isalnum() or
            c.isspace() or
            c in ['.', ',', '!', '?'] for c in value
        ):
            raise ValueError('Описание содержит недопустимые символы.')
        return value


class TaskCreateRequest(TaskBase):
    assignee_id: UUID4 | None = None
    column_id: UUID4 | None = None
    sprint_id: UUID4 | None = None
    board_id: UUID4 | None = None
    group_id: UUID4 | None = None
    watchers: List[UserDB] = []
    executors: List[UserDB] = []


class TaskUpdateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None = Field(None, min_length=3)
    description: str | None = None
    status: Status | None = None
    assignee_id: UUID4 | None = None
    column_id: UUID4 | None = None
    sprint_id: UUID4 | None = None
    board_id: UUID4 | None = None
    group_id: UUID4 | None = None
    watchers: List[UserDB] | None = None
    executors: List[UserDB] | None = None

    @field_validator('description')
    def validate_description(cls, value):
        if value and not all(
            c.isalnum() or
            c.isspace() or
            c in ['.', ',', '!', '?'] for c in value
        ):
            raise ValueError('Описание содержит недопустимые символы.')
        return value


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    created_at: datetime
    assignee_id: UUID4 | None
    column_id: UUID4 | None
    sprint_id: UUID4 | None
    board_id: UUID4 | None
    group_id: UUID4 | None
    watchers: List[UserDB]
    executors: List[UserDB]
