from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user import UserRepository
from app.schemas.schemas import UserOut
from app.api.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return UserRepository(db).list_all()
