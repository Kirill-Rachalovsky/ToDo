from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.user_model import User
from auth.manager import get_user_manager
from database import engine, Base
from auth.schemas import UserCreate, UserRead
from core.crud import todo_router


app = FastAPI()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()


@app.middleware("http")
async def error_log_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code // 100 == 4:
        with open('error_log.txt', 'a') as file:
            file.write(f'{request.method} {request.url} {response.status_code}\n')
    return response


api_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    api_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    api_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    todo_router,
    tags=["boards"]
)

