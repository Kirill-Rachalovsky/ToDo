from database import Base
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, DATE
from datetime import datetime


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


class Boards(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    is_done = Column(Boolean, default=False)
    task_text = Column(String, nullable=False)
    date_created = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    date_update = Column(DATE, default=datetime.today().strftime("%Y-%m-%d"))
    board_id = Column(Integer, ForeignKey("boards.id"))


