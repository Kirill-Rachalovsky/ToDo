from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from todo_app.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
