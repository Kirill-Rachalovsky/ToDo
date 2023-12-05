from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import models
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from database import engine, SessionLocal, Base
from typing import Annotated
from schemas import TaskBase, BoardsBase, TaskUpdateBase
from auth.schemas import UserCreate, UserRead


api_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI()

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


current_user = api_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@app.get("/boards")
async def get_all_boards(db: db_dependency):
    results = await db.execute(select(models.Boards))
    boards = results.scalars().all()
    if not boards:
        raise HTTPException(status_code=404, detail="Boards is not found")
    return boards


@app.get("/boards/{board_id}")
async def get_board(board_id: int, db: db_dependency):
    results = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    board = results.scalar()

    if not board:
        raise HTTPException(status_code=404, detail="Board is not found")

    result_of_tasks = await db.execute(select(models.Tasks).where(models.Tasks.board_id == board_id))
    boards_tasks = result_of_tasks.scalars().all()

    result = {
        "board_id": board.id,
        "board_title": board.title,
        "tasks": boards_tasks
    }
    return result


@app.post("/boards")
async def create_board(board: BoardsBase, db: db_dependency):
    db_board = models.Boards(title=board.title)
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    for task in board.tasks:
        db_task = models.Tasks(
            is_done=task.is_done,
            task_text=task.task_text,
            date_created=task.date_created,
            date_update=task.date_update,
            board_id=db_board.id
        )
        db.add(db_task)
    await db.commit()
    return db_board


@app.post("/boards/{board_id}")
async def create_task(board_id: int, task: TaskBase, db: db_dependency):
    db_task = models.Tasks(
        is_done=task.is_done,
        task_text=task.task_text,
        date_created=datetime.today().strftime("%Y-%m-%d"),
        date_update=datetime.today().strftime("%Y-%m-%d"),
        board_id=board_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


@app.delete("/boards/{board_id}")
async def delete_board(board_id: int, db: db_dependency):
    results = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = results.scalar()
    if not db_board:
        raise HTTPException(status_code=404, detail="Boards is not found")

    result_of_tasks = await db.execute(select(models.Tasks).where(models.Tasks.board_id == board_id))
    boards_tasks = result_of_tasks.scalars().all()
    if len(boards_tasks) != 0:
        for task in boards_tasks:
            result = await db.execute(select(models.Tasks).where(models.Tasks.id == task.id))
            db_task = result.scalar()
            await db.delete(db_task)
        await db.commit()
    await db.refresh(db_board)
    await db.delete(db_board)
    await db.commit()


@app.put("/boards/{board_id}")
async def update_board(board_id: int, new_title:str, db: db_dependency):
    results = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = results.scalar()

    if not db_board:
        raise HTTPException(status_code=404, detail="Boards is not found")

    db_board.title = new_title
    await db.commit()
    await db.refresh(db_board)
    return db_board


@app.delete("/boards/{board_id}/{task_id}")
async def delete_task(board_id: int, task_id: int, db: db_dependency):

    result = await db.execute(select(models.Tasks).where(models.Tasks.id == task_id))
    db_task = result.scalar()

    result = await db.execute(select(models.Boards).where(models.Boards.id == db_task.board_id))
    db_board = result.scalar()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")

    await db.delete(db_task)
    await db.commit()
    await db.refresh(db_board)


@app.put("/boards/{board_id}/{task_id}")
async def update_task(board_id: int, task_id: int, task: TaskUpdateBase, db: db_dependency):
    query = await db.execute(select(models.Tasks).where(models.Tasks.id == task_id))
    db_task = query.scalar()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")

    db_task.is_done = task.is_done
    db_task.task_text = task.task_text
    db_task.date_update = datetime.today()
    await db.commit()
    await db.refresh(db_task)

