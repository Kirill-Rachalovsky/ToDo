import pytest
from httpx import AsyncClient

from core.models import StatusEnum


@pytest.fixture()
async def user_data():
    return {
        "email": "USER",
        "password": "PASS",
        "username": "user",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }


@pytest.fixture()
async def board_data():
    return {
        "title": "My board",
        "tasks": [
            {
                "status": StatusEnum.NOT_STARTED.value,
                "task_text": "Do homework"
            },
            {
                "status": StatusEnum.NOT_STARTED.value,
                "task_text": "Make dinner"
            },
            {
                "status": StatusEnum.NOT_STARTED.value,
                "task_text": "Clean the room"
            }
        ]
    }


@pytest.fixture()
async def board_update_data():
    return {
        "new_title": "My new Board"
    }


@pytest.fixture()
async def task_data():
    return {
        "status": StatusEnum.NOT_STARTED.value,
        "task_text": "Task text"
    }


@pytest.fixture()
async def task_update_data():
    return {
        "status": StatusEnum.DONE.value,
        "task_text": "New task text"
    }


@pytest.mark.anyio
async def test_user_register(async_client: AsyncClient, user_data):
    response = await async_client.post("auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == user_data["username"]


@pytest.mark.anyio
async def test_user_login(async_client: AsyncClient, user_data):
    response = await async_client.post(
        "auth/jwt/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert response.status_code == 204


@pytest.mark.anyio
async def test_create_board(async_client: AsyncClient, get_token, board_data):
    response = await async_client.post(
        "/boards",
        json=board_data,
        cookies=get_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == board_data["title"]


@pytest.mark.anyio
async def test_get_all_boards(async_client: AsyncClient, get_token):
    response = await async_client.get(
        "/boards",
        cookies=get_token
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_board(async_client: AsyncClient, get_token, board_data):
    response = await async_client.get(
        "/boards/1",
        cookies=get_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data["board_title"] == board_data["title"]


@pytest.mark.anyio
async def test_update_board(async_client: AsyncClient, get_token, board_data, board_update_data):
    response = await async_client.put(
        "/boards/1",
        params=board_update_data,
        cookies=get_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] != board_data["title"]
    assert data["title"] == board_update_data["new_title"]


@pytest.mark.anyio
async def test_create_task(async_client: AsyncClient, get_token, task_data):
    response = await async_client.post(
        "/boards/1",
        json=task_data,
        cookies=get_token
    )
    assert response.status_code == 201


@pytest.mark.anyio
async def test_update_task(async_client: AsyncClient, get_token, task_update_data):
    response = await async_client.put(
        "/boards/1/1",
        json=task_update_data,
        cookies=get_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == task_update_data["status"]
    assert data["task_text"] == task_update_data["task_text"]


@pytest.mark.anyio
async def test_delete_board(async_client: AsyncClient, get_token):
    response = await async_client.delete(
        "/boards/1",
        cookies=get_token
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_user_logout(async_client: AsyncClient, get_token):

    response = await async_client.post(
        "auth/jwt/logout",
        cookies=get_token
    )
    assert response.status_code == 204
