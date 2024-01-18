from datetime import datetime

from pydantic import BaseModel, Field
from typing_extensions import List


class Task(BaseModel):
    id: int
    status: str
    data_created: datetime
    data_complete: datetime


class UserStatistic(BaseModel):
    user_id: int
    username: str = Field(max_length=30)
    email: str = Field(max_length=50)
    tasks: List[Task] = Field(default_factory=list)
    amount_deleted_tasks: int

