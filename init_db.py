from sqlalchemy.ext.asyncio import create_async_engine
from domain.models import Base


DATABASE_URL = "postgresql+asyncpg://postgres:admin@db:5432/parking"

engine = create_async_engine(DATABASE_URL, echo=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
