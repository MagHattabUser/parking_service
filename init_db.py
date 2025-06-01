from sqlalchemy.ext.asyncio import create_async_engine
from domain.models import Base
from web.config import Configs

# Получаем URL базы данных из общего конфигурационного файла
config = Configs()
DATABASE_URL = config.DATABASE_URL

print(f"Connecting to database at: {DATABASE_URL}")
engine = create_async_engine(DATABASE_URL, echo=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
