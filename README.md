# Сервис: Управление парковочными зонами
Этот проект представляет собой веб-приложение на базе FastAPI для управления парковочными зонами и местами. Приложение использует PostgreSQL в качестве базы данных и Docker для удобного развертывания

## Основные функции
* Создание и управление парковочными зонами

* Добавление и удаление парковочных мест

* Хранение данных о парковочных зонах и местах в базе данных PostgreSQL

## Технологии
* FastAPI — веб-фреймворк для создания API

* PostgreSQL — реляционная база данных

* SQLAlchemy — ORM для работы с базой данных

* Docker — контейнеризация приложения и базы данных

* Uvicorn — ASGI-сервер для запуска FastAPI

Структура проекта
````
├── Dockerfile
├── README.md
├── __pycache__
├── application
│   └── services
├── db_init.py
├── docker-compose.yml
├── domain
│   ├── __pycache__
│   ├── i_base.py
│   ├── i_parking_place.py
│   ├── i_parking_zone.py
│   └── models.py
├── infrastructure
│   ├── __pycache__
│   ├── database.py
│   └── repositories
├── requirements.txt
└── web
    ├── __pycache__
    ├── config.py
    ├── container.py
    ├── handlers
    ├── main.py
    ├── mapper.py
    └── schemas.py
````
# Установка и запуска
1. Клонировать репозиторий
````
git clone https://github.com/MagHattabUser/parking_service.git
cd parking_service
````
2. Соберите и запустите контейнеры с помощью Docker Compose:
````
docker-compose up --build
````
Это создаст и запустит два контейнера:

* postgres_db — контейнер с PostgreSQL

* fastapi_app — контейнер с FastAPI приложением
3. После запуска приложение будет доступно по адресу:
````
http://localhost:8000
````
4. Чтобы остановить контейнеры, выполните:
````
docker-compose down
````
# Инициализация базы данных
При первом запуске база данных и таблицы будут автоматически созданы с помощью скрипта init_db.py