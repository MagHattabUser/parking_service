from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, model, model_id: int):
        result = await self.db.execute(select(model).where(model.id == model_id))
        return result.scalars().first()

    async def save(self, instance):
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance):
        await self.db.delete(instance)
        await self.db.commit()
