from pydantic.v1 import BaseSettings


class Configs(BaseSettings):
    SQLite_CONNECTION_URI: str = "sqlite+aiosqlite:///./parking.db"

    class Config:
        env_file = ".env"