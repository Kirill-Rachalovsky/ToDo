from datetime import date
from typing import List, Optional

from pydantic import BaseModel, PastDate


class TaskBase(BaseModel):
    is_done: bool=False
    task_text: str = 'Task text'
    date_created: date
    date_update: date


class TaskUpdateBase(BaseModel):
    is_done: Optional[bool] = False
    task_text: Optional[str]


class BoardsBase(BaseModel):
    title: str = 'Enter a board title'
    tasks: List[TaskBase]

