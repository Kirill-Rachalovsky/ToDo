from database import Base
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, DATE
from datetime import datetime


class Boards(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean, default=False)
    task_text = Column(String, nullable=False)
    date_created = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    date_update = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    board_id = Column(Integer, ForeignKey("boards.id"))


