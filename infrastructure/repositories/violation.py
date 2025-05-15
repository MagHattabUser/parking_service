from sqlalchemy.future import select
from datetime import datetime

from domain.i_violation import IViolation
from infrastructure.repositories.base import BaseRepository
from domain.models import Violation

class ViolationRepository(BaseRepository, IViolation):
    async def list_by_place(self, place_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(Violation).where(Violation.parking_place_id == place_id))
        return result.scalars().all()

    async def list_by_date_range(self, start: datetime, end: datetime):
        async with self.db.get_session() as session:
            result = await session.execute(select(Violation).where(Violation.timestamp.between(start, end)))
        return result.scalars().all()
