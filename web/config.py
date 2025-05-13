from pydantic.v1 import BaseSettings


class Configs(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://admin:secret@localhost:5432/mydb"
    JWT_SECRET_KEY: str = "44b46c7d69279c7ee01ed9147704ed78190a5ff9c1560c910a562ec60f9b06b0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # Токен обновления действителен 30 дней

    class Config:
        env_file = ".env"