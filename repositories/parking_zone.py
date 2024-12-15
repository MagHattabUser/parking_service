from sqlalchemy import delete
from sqlalchemy.future import select
from .base import BaseRepository
from models import ParkingZone, ParkingPlace

class ParkingZoneRepository(BaseRepository):
    async def get_all(self):
        result = await self.db.execute(select(ParkingZone))
        return result.scalars().all()

    async def delete_by_id_or_name(self, identifier: str | int):
        query = select(ParkingZone)

        if isinstance(identifier, int):
            query = query.where(ParkingZone.id == identifier)
        elif isinstance(identifier, str):
            query = query.where(ParkingZone.name == identifier)

        result = await self.db.execute(query)
        zone = result.scalars().first()

        if zone:
            await self.db.execute(delete(ParkingPlace).where(ParkingPlace.zone_id == zone.id))

            await self.delete(zone)
            return zone
        else:
            return None