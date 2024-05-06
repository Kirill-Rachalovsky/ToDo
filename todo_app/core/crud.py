from datetime import datetime

from fastapi import HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app.auth.auth import auth_backend
from todo_app.auth.manager import get_user_manager
from todo_app.auth.user_model import User
from todo_app.core import models
from todo_app.core.models import StatusEnum
from todo_app.core.schemas import BoardsBase, TaskBase

api_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


async def create_board(db: AsyncSession, user: User, board: BoardsBase):
    db_board = models.Boards(
        title=board.title,
        user_id=user.id,
    )
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    return db_board


async def get_all_boards(db: AsyncSession, user: User):
    query = await db.execute(select(models.Boards).where(models.Boards.user_id == user.id))
    boards = query.scalars().all()

    if not boards:
        raise HTTPException(status_code=404, detail="Boards is not found")

    return boards


async def get_board(db: AsyncSession, user: User, board_id: int):
    board_query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    board = board_query.scalar()

    if not board or board.user_id != user.id:
        raise HTTPException(status_code=404, detail="Board is not found")

    task_query = await db.execute(select(models.Tasks).where(models.Tasks.board_id == board_id))
    boards_tasks = task_query.scalars().all()
    result = {
        "board_id": board.id,
        "board_title": board.title,
        "tasks": boards_tasks
    }
    return result


async def update_board(db: AsyncSession, user: User, board_id: int, new_title: str):
    query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = query.scalar()

    if not db_board or db_board.user_id != user.id:
        raise HTTPException(status_code=404, detail="Board is not found")

    db_board.title = new_title
    await db.commit()
    await db.refresh(db_board)
    return db_board


async def delete_board(db: AsyncSession, user: User, board_id: int):
    board_query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = board_query.scalar()

    if not db_board or db_board.user_id != user.id:
        raise HTTPException(status_code=404, detail="Boards is not found")

    tasks_query = await db.execute(select(models.Tasks).where(models.Tasks.board_id == board_id))
    boards_tasks = tasks_query.scalars().all()

    deleted_tasks_list = []

    if len(boards_tasks) != 0:
        for task in boards_tasks:
            result = await db.execute(select(models.Tasks).where(models.Tasks.id == task.id))
            db_task = result.scalar()
            deleted_tasks_list.append(db_task.id)
            await db.delete(db_task)
        await db.commit()
    await db.refresh(db_board)
    await db.delete(db_board)
    await db.commit()

    return deleted_tasks_list


async def create_task(db: AsyncSession, user: User, board_id: int, task: TaskBase):
    # current_user не используется, но он не допускает к Эндпоинту неавторизированных пользователей
    if task.status not in StatusEnum:
        raise HTTPException(
            status_code=500,
            detail=f'You should choice task status from {StatusEnum.get_allowed_statuses()}'
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


async def update_task(db: AsyncSession, user: User,
                      board_id: int, task_id: int, task: TaskBase):
    task_query = await db.execute(select(models.Tasks).where(models.Tasks.id == task_id))
    db_task = task_query.scalar()
    board_query = await db.execute(select(models.Boards).where(models.Boards.id == board_id))
    db_board = board_query.scalar()

    if not db_task or db_board.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")
    elif task.status not in StatusEnum:
        raise HTTPException(
            status_code=500,
            detail=f'You should choice task status from {StatusEnum.get_allowed_statuses()}'
        )

    db_task.status = task.status
    db_task.task_text = task.task_text
    db_task.date_update = datetime.today()
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, user: User, board_id: int, task_id: int):
    task_query = await db.execute(select(models.Tasks).where(models.Tasks.id == task_id))
    db_task = task_query.scalar()
    board_query = await db.execute(select(models.Boards).where(models.Boards.id == db_task.board_id))
    db_board = board_query.scalar()

    if not db_task or db_board.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")

    await db.delete(db_task)
    await db.commit()
    await db.refresh(db_board)
