from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app.auth.auth import auth_backend
from todo_app.auth.manager import get_user_manager
from todo_app.auth.user_model import User
from todo_app.core import crud
from todo_app.core.schemas import BoardsCreate, TasksCreate
from todo_app.database import get_db

api_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = api_users.current_user()

todo_router = APIRouter()


@todo_router.post("/boards", status_code=201)
async def create_board_service(board: BoardsCreate, db: AsyncSession = Depends(get_db),
                               user: User = Depends(current_user)):
    _board = await crud.create_board(db, user, board=board.parameter)
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
    await crud.delete_board(db, user, board_id)
    return {'message': "Board delete successfully"}


@todo_router.post("/boards/{board_id}", status_code=201)
async def create_task_service(board_id: int, task: TasksCreate, db: AsyncSession = Depends(get_db),
                              user: User = Depends(current_user)):
    _task = await crud.create_task(db, user, board_id, task)
    return {
        'message': "Task Created successfully",
        'details': _task
    }


@todo_router.put("/boards/{board_id}/{task_id}", status_code=201)
async def update_task_service(board_id: int, task_id: int, task: TasksCreate, db: AsyncSession = Depends(get_db),
                              user: User = Depends(current_user)):
    _task = await crud.update_task(db, user, board_id, task_id, task)
    return _task


@todo_router.delete("/boards/{board_id}/{task_id}")
async def delete_task_service(board_id: int, task_id: int, db: AsyncSession = Depends(get_db),
                              user: User = Depends(current_user)):
    await crud.delete_task(db, user, board_id, task_id)
    return {'message': "Task deleted successfully"}
