from fastapi import FastAPI
from app.database import engine, Base
from app.api import auth_router, tasks_router, admin_router
from app.repositories.user import UserRepository
from app.database import SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        if not repo.get_by_username("admin"):
            repo.create(
                email="admin@example.com",
                username="admin",
                phone="+7-900-000-00-00",
                password="Admin123",
                role="admin"
            )
    finally:
        db.close()

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(admin_routerr)  # ОШИБКА: admin_routerr вместо admin_router

@app.get("/")
def root():
    return {"message": "Task Tracker API is running"}
