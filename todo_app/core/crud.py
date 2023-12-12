from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, SessionLocal, Base
from core.schemas import BoardsBase, TaskBase
from core import models
from core.models import StatusEnum, get_allowed_statuses


async def get_db():
    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


todo_router = APIRouter()


# CREATE BOARD
@todo_router.post("/boards")
async def create_board(board: BoardsBase, db: db_dependency):
    db_board = models.Boards(title=board.title)
    db.add(db_board)
    # TODO Удалить комиты в середине транзакции, чтобы сделать её атомарной
    await db.commit()
    await db.refresh(db_board)
    for task in board.tasks:

        if task.status not in StatusEnum:
            raise HTTPException(
                status_code=500,
                detail=f'You should choice task status from {get_allowed_statuses()}'
            )

        db_task = models.Tasks(
            status=task.status,
            task_text=task.task_text,
            date_created=datetime.today(),
            date_update=datetime.today(),
            board_id=db_board.id
        )
        db.add(db_task)
    await db.commit()
    return db_board


# GET ALL BOARDS
@todo_router.get("/boards")
async def get_all_boards(db: db_dependency):
    query = await db.execute(select(models.Boards))
    boards = query.scalars().all()
    if not boards:
        raise HTTPException(status_code=404, detail="Boards is not found")
    return boards


# GET BOARD WITH TASKS
@todo_router.get("/boards/{board_id}")
async def get_board(board_id: int, db: db_dependency):
    board_query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    board = board_query.scalar()
    if not board:
        raise HTTPException(status_code=404, detail="Board is not found")
    task_query = await db.execute(select(models.Tasks).where(models.Tasks.board_id == board_id))
    boards_tasks = task_query.scalars().all()
    result = {
        "board_id": board.id,
        "board_title": board.title,
        "tasks": boards_tasks
    }
    return result


# UPDATE BOARD
@todo_router.put("/boards/{board_id}")
async def update_board(board_id: int, new_title:str, db: db_dependency):
    query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = query.scalar()
    db_board.title = new_title
    await db.commit()
    await db.refresh(db_board)
    return db_board


# DELETE BOARD
@todo_router.delete("/boards/{board_id}")
async def delete_board(board_id: int, db: db_dependency):
    board_query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = board_query.scalar()
    if not db_board:
        raise HTTPException(status_code=404, detail="Boards is not found")

    tasks_query = await db.execute(select(models.Tasks).where(models.Tasks.board_id == board_id))
    boards_tasks = tasks_query.scalars().all()
    if len(boards_tasks) != 0:
        for task in boards_tasks:
            result = await db.execute(select(models.Tasks).where(models.Tasks.id == task.id))
            db_task = result.scalar()
            await db.delete(db_task)
        await db.commit()
    await db.refresh(db_board)
    await db.delete(db_board)
    await db.commit()


# CREATE TASK
@todo_router.post("/boards/{board_id}")
async def create_task(board_id: int, task: TaskBase, db: db_dependency):
    if task.status not in StatusEnum:
        raise HTTPException(
            status_code=500,
            detail=f'You should choice task status from {get_allowed_statuses()}'
        )
    db_task = models.Tasks(
        status=task.status,
        task_text=task.task_text,
        date_created=datetime.today(),
        date_update=datetime.today(),
        board_id=board_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


# UPDATE TASK
@todo_router.put("/boards/{board_id}/{task_id}")
async def update_task(board_id: int, task_id: int, task: TaskBase, db: db_dependency):
    query = await db.execute(select(models.Tasks).where(models.Tasks.id == task_id))
    db_task = query.scalar()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")
    elif task.status not in StatusEnum:
        raise HTTPException(
            status_code=500,
            detail=f'You should choice task status from {get_allowed_statuses()}'
        )

    db_task.status = task.status
    db_task.task_text = task.task_text
    db_task.date_update = datetime.today()
    await db.commit()
    await db.refresh(db_task)


# DELETE TASK
@todo_router.delete("/boards/{board_id}/{task_id}")
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


