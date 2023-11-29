from datetime import datetime

from fastapi import FastAPI, status, HTTPException, Depends
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import TaskBase, BoardsBase


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/boards")
def get_all_boards(db: db_dependency):
    result = db.query(models.Boards).all()
    if not result:
        raise HTTPException(status_code=404, detail="Boards is not found")
    return result


@app.get("/boards/{board_id}")
def get_board(board_id: int, db: db_dependency):
    board = db.query(models.Boards).filter(models.Boards.id == board_id).first()

    if not board:
        raise HTTPException(status_code=404, detail="Board is not found")

    boards_tasks = db.query(models.Tasks).filter(models.Tasks.board_id == board_id).all()
    result = {
        "board_id": board.id,
        "board_title": board.title,
        "tasks": boards_tasks
    }
    return result


@app.post("/boards")
def create_board(board: BoardsBase, db: db_dependency):
    db_board = models.Boards(title=board.title)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    for task in board.tasks:
        db_task = models.Tasks(
            is_done=task.is_done,
            task_text=task.task_text,
            date_created=task.date_created,
            date_update=task.date_update,
            board_id=db_board.id
        )
        db.add(db_task)
    db.commit()
    return db_board


@app.post("/boards/{board_id}")
def create_task(board_id: int, task: TaskBase, db: db_dependency):
    db_task = models.Tasks(
        is_done=task.is_done,
        task_text=task.task_text,
        date_created=datetime.today().strftime("%Y-%m-%d"),
        date_update=datetime.today().strftime("%Y-%m-%d"),
        board_id=board_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/boards/{board_id}")
def delete_board(board_id: int, db: db_dependency):
    db_board = db.query(models.Boards).filter(models.Boards.id == board_id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Boards is not found")

    boards_tasks = db.query(models.Tasks).filter(models.Tasks.board_id == board_id).all()
    if len(boards_tasks) != 0:
        for task in boards_tasks:
            db_task = db.query(models.Tasks).filter(models.Tasks.id == task.id).first()
            db.delete(db_task)
        db.commit()
    db.refresh(db_board)
    db.delete(db_board)
    db.commit()


@app.put("/boards/{board_id}")
def update_board(board_id: int, new_title:str, db: db_dependency):
    db_board = db.query(models.Boards).filter(models.Boards.id == board_id).first()

    if not db_board:
        raise HTTPException(status_code=404, detail="Boards is not found")

    db_board.title = new_title
    db.commit()
    db.refresh(db_board)
    return db_board


@app.delete("/boards/{board_id}/{task_id}")
def delete_task(board_id: int, task_id: int, db: db_dependency):
    db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    db_board = db.query(models.Boards).filter(models.Boards.id == board_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")

    db.delete(db_task)
    db.commit()
    db.refresh(db_board)
    return {
        "board_id": db_board.id,
        "board_title": db_board.title,
        "tasks": db.query(models.Tasks).filter(models.Tasks.board_id == board_id).all()
    }


@app.put("/boards/{board_id}/{task_id}")
def update_task(board_id: int, task_id: int, new_task_text: str, done_status: bool, db: db_dependency):
    db_task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task is not found")
    elif db_task.board_id != board_id:
        raise HTTPException(status_code=404, detail="This board does not contain such a task")

    db_task.is_done = done_status
    db_task.task_text = new_task_text
    db_task.date_update = datetime.today().strftime("%Y-%m-%d")
    db.commit()
    return db_task

