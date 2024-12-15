from sqlalchemy import select
from sqlalchemy.orm.loading import instances
from .base import BaseRepository
from models import ParkingPlace, ParkingZone


class ParkingPlaceRepository(BaseRepository):
    async def get_by_zone(self, zone_identifier: str | int):
        query = select(ParkingPlace).join(ParkingZone)

        if isinstance(zone_identifier, int):
            query = query.where(ParkingZone.id == zone_identifier)
        elif isinstance(zone_identifier, str):
            query = query.where(ParkingZone.name == zone_identifier)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_all(self):
        result = await self.db.execute(select(ParkingZone))
        return result.scalars().all()

    async def delete_by_id(self, place_id: int):
        query = select(ParkingPlace).where(ParkingPlace.id == place_id)
        result = await self.db.execute(query)
        place = result.scalars().first()

        if place:
            await self.delete(place)
            return place
        else:
            return None
