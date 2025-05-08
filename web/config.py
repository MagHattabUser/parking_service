from pydantic.v1 import BaseSettings


class Configs(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://admin:secret@localhost:5432/mydb"

    class Config:
        env_file = ".env"