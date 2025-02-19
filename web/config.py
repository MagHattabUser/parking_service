from pydantic.v1 import BaseSettings


class Configs(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/parking"

    class Config:
        env_file = ".env"