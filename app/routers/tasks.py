from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app import crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task_data=task_data)


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return crud.get_all_tasks(db=db, status=status, category=category)


@router.get("/today", response_model=list[TaskResponse])
def get_today_tasks(db: Session = Depends(get_db)):
    return crud.get_today_tasks(db=db)


@router.get("/overdue", response_model=list[TaskResponse])
def get_overdue_tasks(db: Session = Depends(get_db)):
    return crud.get_overdue_tasks(db=db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db=db, task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db=db, task_id=task_id, task_data=task_data)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.complete_task(db=db, task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db=db, task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": f"Task with id {task_id} was deleted"}