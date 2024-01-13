from typing import List

from pydantic import BaseModel, Field

from todo_app.core.models import StatusEnum


class TaskBase(BaseModel):
    status: str = StatusEnum.NOT_STARTED
    task_text: str = 'Task text'


class BoardsBase(BaseModel):
    title: str = 'Enter a board title'
    tasks: List[TaskBase]


class BoardsCreate(BoardsBase):
    parameter: BoardsBase = Field()


class TasksCreate(TaskBase):
    parameter: TaskBase = Field()
