from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm.sync import update

from .base import BaseRepository
from models import ParkingZone, ParkingPlace
from ..i_parking_zone import IParkingZone


class ParkingZoneRepository(BaseRepository, IParkingZone):
    async def get_all(self):
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingZone))
        return result.scalars().all()

    async def delete_by_id_or_name(self, identifier: str | int):
        query = select(ParkingZone)

        if isinstance(identifier, int):
            query = query.where(ParkingZone.id == identifier)
        elif isinstance(identifier, str):
            query = query.where(ParkingZone.name == identifier)

        async with self.db.get_session() as session:
            result = await session.execute(query)
        zone = result.scalars().first()

        if not zone:
            return None
        async with self.db.get_session() as session:
            await session.execute(delete(ParkingPlace).where(ParkingPlace.zone_id == zone.id))

        await self.delete(zone)
        return zone