from sqlalchemy.future import select
from .base import BaseRepository
from models import ParkingZone

class ParkingZoneRepository(BaseRepository):
    async def get_all(self):
        result = await self.db.execute(select(ParkingZone))
        return result.scalars().all()
