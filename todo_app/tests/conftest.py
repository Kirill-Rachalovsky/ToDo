import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from todo_app.database import engine, Base
from todo_app.main import web_app


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=web_app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture()
async def get_token(async_client) -> dict:
    client_token = dict(fastapiusersauth=str(async_client.cookies.jar)[36:193])
    return client_token
