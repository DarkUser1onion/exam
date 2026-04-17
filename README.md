# Task Tracker API

REST API для управления задачами с регистрацией, JWT-аутентификацией, ролевой моделью и кэшированием через Redis.

## Стек технологий

- FastAPI (Python 3.12)
- PostgreSQL 15
- SQLAlchemy 2.0 (async)
- Redis 7
- JWT (python-jose)
- bcrypt (passlib)
- Pydantic v2
- Docker / Docker Compose

## Структура проекта

~/D/exam ❯❯❯ tree -I '__pycache__|*.pyc|.git|.venv|README_assets|data|app.db'                                                                                                        master
.
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── deps.py
│   │   └── tasks.py
│   ├── config.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── redis_client.py
│   │   └── security.py
│   ├── database.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── models.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── user.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── task.py
│   └── utils
│       └── __init__.py
├── docker-compose.yml
└── requirements.txt

9 directories, 27 files
~/D/exam ❯❯❯ 

## Запуск через Docker Compose

1. Убедиться, что установлены Docker и Docker Compose.
2. Клонировать репозиторий:

git clone https://github.com/DarkUser1onion/exam.git
cd exam

3. Запустить контейнеры:

docker-compose up --build

4. После успешного запуска Swagger UI доступен по адресу:
http://localhost:8000/docs

## Учетные записи по умолчанию

При первом запуске автоматически создается администратор:

- Логин: `admin`
- Пароль: `Admin123`

Обычные пользователи создаются через эндпоинт регистрации.

## Основные эндпоинты API

### Аутентификация

| Метод | Путь           | Описание                              |
|-------|----------------|-------------------------------------------------------------|
| POST  | /auth/register | Регистрация нового пользователя       |
| POST  | /auth/login    | Получение JWT (access token)          |
| GET   | /auth/me       | Информация о текущем пользователе     |

### Задачи

| Метод | Путь          | Описание                               |
|------|----------------|-----------------------------------------------------------------------|
| POST  | /tasks/       | Создание новой задачи                      |
| GET   | /tasks/       | Список задач текущего пользователя         |
| GET   | /tasks/{id}   | Получение задачи по идентификатору         |
| PATCH | /tasks/{id}   | Частичное обновление задачи                |
| DELETE| /tasks/{id}   | Удаление задачи                            |

Список задач кэшируется в Redis (TTL 60 секунд).

### Администрирование (только роль `admin`)

| Метод | Путь          | Описание                |
|------|----------------|-------------------------------|
| GET   | /admin/users  | Список всех пользователей |

## Переменные окружения

Настройки приложения задаются через переменные окружения (в `docker-compose.yml` или `.env`):

| Переменная                 | Назначение                       | Значение по умолчанию                     |
|-----------------------------|------------------------------------|------------------------------------------------------------------|
| DATABASE_URL               | Строка подключения к БД          | postgresql://postgres:postgres@db/exam_db |
| REDIS_URL                  | Адрес Redis                      | redis://redis:6379/0                      |
| SECRET_KEY                 | Ключ для подписи JWT             | change_this_in_production_123!             |
| ACCESS_TOKEN_EXPIRE_MINUTES| Время жизни access токена (мин)  | 60                                         |
