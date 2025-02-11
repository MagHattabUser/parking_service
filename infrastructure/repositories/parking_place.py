from sqlalchemy import select
from .base import BaseRepository
from domain.models import ParkingPlace, ParkingZone
from domain.i_parking_place import IParkingPlace


class ParkingPlaceRepository(BaseRepository, IParkingPlace):
    async def get_by_zone(self, zone_identifier: str | int):
        query = select(ParkingPlace).join(ParkingZone)

        if isinstance(zone_identifier, int):
            query = query.where(ParkingZone.id == zone_identifier)
        elif isinstance(zone_identifier, str):
            query = query.where(ParkingZone.name == zone_identifier)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return result.scalars().all()

    async def get_all(self):
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingZone))
        return result.scalars().all()

    async def delete_by_id(self, place_id: int):
        query = select(ParkingPlace).where(ParkingPlace.id == place_id)
        async with self.db.get_session() as session:
            result = await session.execute(query)
        place = result.scalars().first()

        if place:
            await self.delete(place)
            return place
        else:
            return None
