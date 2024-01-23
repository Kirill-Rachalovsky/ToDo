from contextlib import asynccontextmanager

from dotenv import dotenv_values
from fastapi import FastAPI, Request, HTTPException

from statistic.database import DatabaseManager
from statistic.router import statistic_router

config = dotenv_values(".env_mongo")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = DatabaseManager()
    app.mongo_db = app.client.collection
    yield
    app.client.close_db()


stat_app = FastAPI(lifespan=lifespan)


@stat_app.middleware("http")
async def auth_check_middleware(request: Request, call_next):
    token = request.cookies.get('fastapiusersauth')
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    response = await call_next(request)
    return response


stat_app.include_router(
    statistic_router,
    tags=['statistic']
)
