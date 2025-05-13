from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database import Database
from domain.i_base import IBase


class BaseRepository(IBase):
    def __init__(self, db: Database):
        self.db = db

    async def get_by_id(self, model, model_id: int):
        primary_key = model.__mapper__.primary_key[0]
        async with self.db.get_session() as session:
            result = await session.execute(select(model).where(primary_key == model_id))
        return result.scalars().first()

    async def get_by_all(self, model):
        """Получение всех записей модели"""
        async with self.db.get_session() as session:
            result = await session.execute(select(model))
        return result.scalars().all()

    async def save(self, instance):
        async with self.db.get_session() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance

    async def update(self, instance):
        """Обновление существующей записи"""
        async with self.db.get_session() as session:
            merged_instance = await session.merge(instance)
            await session.commit()
            await session.refresh(merged_instance)
        return merged_instance

    async def delete(self, instance):
        async with self.db.get_session() as session:
            await session.delete(instance)
            await session.commit()
