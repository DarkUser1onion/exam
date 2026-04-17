from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.task import TaskService
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskOut
from app.api.deps import get_current_user
from app.models.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).create_task(current_user.id, data)

@router.get("/", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).list_tasks(current_user.id)

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).get_task_for_user(task_id, current_user)

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskService(db).update_task(task_id, data, current_user)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    TaskService(db).delete_task(task_id, current_user)
    return {"message": "Задача удалена"}
