from datetime import date
from typing import List

from pydantic import BaseModel, PastDate


class TaskBase(BaseModel):
    is_done: bool=False
    task_text: str = 'Task text'
    date_created: date
    date_update: date


class BoardsBase(BaseModel):
    title: str = 'Enter a board title'
    tasks: List[TaskBase]

