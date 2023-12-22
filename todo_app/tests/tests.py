import pytest
from httpx import AsyncClient

from data import user_payload, board_payload, board_update_payload, task_payload, task_update_payload

client_token = dict()


@pytest.mark.anyio
async def test_user_register(async_client: AsyncClient):
    response = await async_client.post("auth/register", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == user_payload["username"]


@pytest.mark.anyio
async def test_user_login(async_client: AsyncClient):
    response = await async_client.post(
        "auth/jwt/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"]
        }
    )
    assert response.status_code == 204

    # SETUP token for authorization
    global client_token
    client_token = {"fastapiusersauth": str(async_client._cookies.jar)[36:193]}


@pytest.mark.anyio
async def test_create_board(async_client: AsyncClient):
    response = await async_client.post(
        "/boards",
        json=board_payload,
        cookies=client_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == board_payload["title"]


@pytest.mark.anyio
async def test_get_all_boards(async_client: AsyncClient):
    response = await async_client.get(
        "/boards",
        cookies=client_token
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_board(async_client: AsyncClient):
    response = await async_client.get(
        "/boards/1",
        cookies=client_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data["board_title"] == board_payload["title"]


@pytest.mark.anyio
async def test_update_board(async_client: AsyncClient):
    response = await async_client.put(
        "/boards/1",
        params=board_update_payload,
        cookies=client_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] != board_payload["title"]
    assert data["title"] == board_update_payload["new_title"]


@pytest.mark.anyio
async def test_create_task(async_client: AsyncClient):
    response = await async_client.post(
        "/boards/1",
        json=task_payload,
        cookies=client_token
    )
    assert response.status_code == 201


@pytest.mark.anyio
async def test_update_task(async_client: AsyncClient):
    response = await async_client.put(
        "/boards/1/1",
        json=task_update_payload,
        cookies=client_token
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == task_update_payload["status"]
    assert data["task_text"] == task_update_payload["task_text"]


@pytest.mark.anyio
async def test_delete_board(async_client: AsyncClient):
    response = await async_client.delete(
        "/boards/1",
        cookies=client_token
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_user_logout(async_client: AsyncClient):
    response = await async_client.post(
        "auth/jwt/logout",
        cookies=client_token
    )
    assert response.status_code == 204
