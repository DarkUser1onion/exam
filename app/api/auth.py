from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import AuthService
from app.schemas.schemas import RegisterRequest, UserOut, LoginResponse
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register_user(data)

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthService(db).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    token = create_access_token({"sub": str(user.id), "role": user.role, "username": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
