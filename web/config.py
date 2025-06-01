from pydantic.v1 import BaseSettings


class Configs(BaseSettings):
    #database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@db:5432/parking"
    #DATABASE_URL: str = "postgresql+asyncpg://admin:secret@localhost:5432/mydb"

    #auth
    JWT_SECRET_KEY: str = "44b46c7d69279c7ee01ed9147704ed78190a5ff9c1560c910a562ec60f9b06b0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    #minio
    MINIO_ENDPOINT = "minio:9000"
    MINIO_ACCESS_KEY = "minioadmin"  # Обновлено в соответствии с docker-compose
    MINIO_SECRET_KEY = "minioadmin"  # Обновлено в соответствии с docker-compose
    MINIO_SECURE = False
    BUCKET_NAME = "car-places"

    #service
    CUTTER_SERVICE_URL = "http://cutter_service:8070"
    DIRECTOR_SERVICE_URL = "http://ml_director:8080"

    #rabbitmq
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"
    DRAW_QUEUE: str = "draw_queue"
    DRAW_RESULT_QUEUE: str = "draw_result_queue"

    class Config:
        env_file = ".env"