from typing import Optional
from typing import AsyncGenerator

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal, configuration

from auth.user_model import User


SECRET = configuration.secret


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)