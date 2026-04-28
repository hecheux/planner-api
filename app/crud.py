from datetime import date

from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

#Work with DB
def create_task(db: Session, task_data: TaskCreate):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        category=task_data.category,
        deadline=task_data.deadline
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_all_tasks(db: Session, status: str | None = None, category: str | None = None):
    query = db.query(Task)

    if status is not None:
        query = query.filter(Task.status == status)

    if category is not None:
        query = query.filter(Task.category == category)

    return query.all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_today_tasks(db: Session):
    today = date.today()
    return db.query(Task).filter(Task.deadline == today).all()


def get_overdue_tasks(db: Session):
    today = date.today()

    return (
        db.query(Task)
        .filter(Task.deadline < today, Task.status != "done")
        .all()
    )


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


def complete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    task.status = "done"
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return task