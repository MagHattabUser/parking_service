from sqlalchemy.future import select

from domain.i_parking_place import IParkingPlace
from infrastructure.repositories.base import BaseRepository
from domain.models import ParkingPlace

class ParkingPlaceRepository(BaseRepository, IParkingPlace):
    async def list_by_zone(self, zone_id: int):
        """Все ParkingPlace для конкретной зоны"""
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingPlace).where(ParkingPlace.parking_zone_id == zone_id))
        return result.scalars().all()

    async def list_by_status(self, status_id: int):
        """Все ParkingPlace с конкретным статусом"""
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingPlace).where(ParkingPlace.place_status_id == status_id))
        return result.scalars().all()