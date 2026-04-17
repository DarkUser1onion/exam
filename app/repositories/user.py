from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.models import User
from app.core.security import hash_password

class UserRepository:
    def __init__(self, db: Session):
        self.session = db  # АТРИБУТ НАЗВАН session, А НЕ db

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()  # ОШИБКА: self.session вместо self.session

    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_by_login(self, login: str):
        return self.session.query(User).filter(
            or_(User.email == login, User.username == login)
        ).first()

    def get_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def list_all(self):
        return self.session.query(User).all()

    def create(self, email: str, username: str, phone: str, password: str, role: str = "user"):
        user = User(
            email=email,
            username=username,
            phone=phone,
            hashed_password=hash_password(password),
            role=role
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
