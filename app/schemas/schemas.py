import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

class RegisterRequest(BaseModel):
    email: str
    username: str
    phone: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$)", v):  # ЛИШНЯЯ СКОБКА В КОНЦЕ
            raise ValueError("Некорректный email")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$", v):
            raise ValueError("Username должен начинаться с буквы и содержать 3-20 символов")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}$", v):
            raise ValueError("Телефон должен быть в формате +7-900-123-45-67")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return v

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    phone: str
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("Название задачи должно содержать минимум 3 символа")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed = {"new", "in_progress", "done"}
        if v not in allowed:
            raise ValueError(f"Статус должен быть одним из: {allowed}")
        return v

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
