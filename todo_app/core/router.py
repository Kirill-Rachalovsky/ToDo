import json

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app.auth.auth import auth_backend
from todo_app.auth.manager import get_user_manager
from todo_app.auth.user_model import User
from todo_app.core import crud
from todo_app.core.schemas import BoardsBase, TaskBase
from todo_app.database import get_db
from todo_app.kafka_messages.maker import *
from todo_app.kafka_messages.producer import producer


api_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = api_users.current_user()

todo_router = APIRouter()


@todo_router.post("/boards", status_code=201)
async def create_board_service(board: BoardsBase, db: AsyncSession = Depends(get_db),
                               user: User = Depends(current_user)):
    _board = await crud.create_board(db, user, board=board)

    return {
        'message': 'Board created successfully',
        'details': _board
    }


@todo_router.get("/boards")
async def get_all_boards_service(db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    _boards = await crud.get_all_boards(db, user)
    return _boards


@todo_router.get("/boards/{board_id}")
async def get_board_service(board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    _board = await crud.get_board(db, user, board_id)
    return _board


@todo_router.put("/boards/{board_id}", status_code=201)
async def update_board_service(board_id: int, new_title: str, db: AsyncSession = Depends(get_db),
                               user: User = Depends(current_user)):
    _board = await crud.update_board(db, user, board_id, new_title)
    return _board


@todo_router.delete("/boards/{board_id}")
async def delete_board_service(board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    deleted_tasks_list = await crud.delete_board(db, user, board_id)
    for task_id in deleted_tasks_list:
        message = json.dumps(delete_task_message(user.id, task_id))
        producer.produce(topic='kafka_messages_topic', key="statistic_update", value=message)
        producer.flush()
    return {'message': "Board delete successfully"}


@todo_router.post("/boards/{board_id}", status_code=201)
async def create_task_service(board_id: int, task: TaskBase, db: AsyncSession = Depends(get_db),
                              user: User = Depends(current_user)):
    _task = await crud.create_task(db, user, board_id, task)

    message = json.dumps(create_task_message(user.id, _task))
    producer.produce(topic='kafka_messages_topic', key="statistic_update", value=message)
    producer.flush()

    return {
        'message': "Task Created successfully",
        'details': _task
    }


@todo_router.put("/boards/{board_id}/{task_id}", status_code=201)
async def update_task_service(board_id: int, task_id: int, task: TaskBase, db: AsyncSession = Depends(get_db),
                              user: User = Depends(current_user)):
    _task = await crud.update_task(db, user, board_id, task_id, task)

    message = json.dumps(update_task_message(user.id, _task))
    producer.produce(topic='kafka_messages_topic', key="statistic_update", value=message)
    producer.flush()

    return _task


@todo_router.delete("/boards/{board_id}/{task_id}")
async def delete_task_service(board_id: int, task_id: int, db: AsyncSession = Depends(get_db),
                              user: User = Depends(current_user)):
    await crud.delete_task(db, user, board_id, task_id)

    message = json.dumps(delete_task_message(user.id, task_id))
    producer.produce(topic='kafka_messages_topic', key="statistic_update", value=message)
    producer.flush()

    return {'message': "Task deleted successfully"}
