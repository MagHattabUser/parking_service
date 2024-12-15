from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, model, model_id: int):
        primary_key = model.__mapper__.primary_key[0]
        result = await self.db.execute(select(model).where(primary_key == model_id))
        return result.scalars().first()

    async def save(self, instance):
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance):
        await self.db.delete(instance)
        await self.db.commit()
