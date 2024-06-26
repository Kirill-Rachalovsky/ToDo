import json
from typing import AsyncGenerator
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app.auth.user_model import User
from todo_app.database import SessionLocal, configuration
from todo_app.kafka_messages.maker import *
from todo_app.kafka_messages.producer import producer


SECRET = configuration.secret


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        message = json.dumps(create_user_message(user))
        producer.produce(topic='kafka_messages_topic', key="statistic_update", value=message)
        producer.flush()
        print(f"User {user.id} has registered.")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
