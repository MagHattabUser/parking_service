from sqlalchemy import select
from sqlalchemy.orm.loading import instances

from .base import BaseRepository
from models import ParkingPlace, ParkingZone


class ParkingPlaceRepository(BaseRepository):
    async def get_by_zone(self, zone_identifier: str | int):
        query = select(ParkingPlace).join(ParkingZone)

        if instances(zone_identifier, int):
            query = query.where(ParkingZone.id == zone_identifier)
        elif instances(zone_identifier, str):
            query = query.where(ParkingZone.name == zone_identifier)

        result = await self.db.execute(query)
        return result.scalar().all()
