from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from todo_app.auth.auth import auth_backend
from todo_app.auth.manager import get_user_manager
from todo_app.auth.schemas import UserCreate, UserRead
from todo_app.auth.user_model import User
from todo_app.core.router import todo_router
from todo_app.database import engine, Base

web_app = FastAPI()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@web_app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


api_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

web_app.include_router(
    api_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

web_app.include_router(
    api_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

web_app.include_router(
    todo_router,
    tags=["boards"]
)
