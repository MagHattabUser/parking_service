from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import Database
from repositories.i_base import IBase


class BaseRepository(IBase):
    def __init__(self, db: Database):
        self.db = db

    async def get_by_id(self, model, model_id: int):
        primary_key = model.__mapper__.primary_key[0]
        async with self.db.get_session() as session:
            result = await session.execute(select(model).where(primary_key == model_id))
        return result.scalars().first()

    async def save(self, instance):
        async with self.db.get_session() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance

    async def delete(self, instance):
        async with self.db.get_session() as session:
            await session.delete(instance)
            await session.commit()