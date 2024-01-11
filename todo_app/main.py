from fastapi import FastAPI, Request, HTTPException
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware

from todo_app.auth.auth import auth_backend
from todo_app.auth.manager import get_user_manager
from todo_app.auth.schemas import UserCreate, UserRead
from todo_app.auth.user_model import User
from todo_app.core.crud import todo_router
from todo_app.database import engine, Base

web_app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@web_app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@web_app.middleware("http")
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
