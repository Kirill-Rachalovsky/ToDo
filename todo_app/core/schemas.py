from pydantic import BaseModel

from todo_app.core.models import StatusEnum


class TaskBase(BaseModel):
    status: str = StatusEnum.NOT_STARTED
    task_text: str = 'Task text'


class BoardsBase(BaseModel):
    title: str = 'Enter a board title'
