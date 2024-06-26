from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, String, Column, ForeignKey, DATE
from sqlalchemy.dialects.postgresql import ENUM

from todo_app.database import Base


class StatusEnum(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    @staticmethod
    def get_allowed_statuses():
        status_list = []
        for i in StatusEnum:
            status_list.append(i.value)
        return status_list


class Boards(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        ENUM(
            StatusEnum,
            name="status__enum",
            create_type=True,
            nullable=False,
            default=StatusEnum.NOT_STARTED
        )
    )
    task_text = Column(String, nullable=False)
    date_created = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    date_update = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    board_id = Column(Integer, ForeignKey("boards.id"))
