from typing import List, Optional, Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.v1.generics import GenericModel


T = TypeVar('T')


class TaskBase(BaseModel):
    status: bool=False
    task_text: str = 'Task text'


class BoardsBase(BaseModel):
    title: str = 'Enter a board title'
    tasks: List[TaskBase]


class RequestBoard(BaseModel):
    parameter: BoardsBase = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
