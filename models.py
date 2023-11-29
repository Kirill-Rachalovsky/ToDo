from database import Base
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, DATE
from datetime import datetime


# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True)
#     hashed_password = Column(String)


class Boards(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    is_done = Column(Boolean, default=False)
    task_text = Column(String, nullable=False)
    date_created = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    date_update = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    board_id = Column(Integer, ForeignKey("boards.id"))


