from typing import List

from sqlalchemy.future import select
from sqlalchemy import and_

from domain.i_parking_zone import IParkingZone
from infrastructure.repositories.base import BaseRepository
from domain.models import ParkingZone

class ParkingZoneRepository(BaseRepository, IParkingZone):
    async def list_by_admin(self, admin_id: int):
        """Все ParkingZone для конкретного администратора"""
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingZone).where(ParkingZone.admin_id == admin_id))
        return result.scalars().all()

    async def list_by_type(self, type_id: int):
        """Все ParkingZone конкретного типа"""
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingZone).where(ParkingZone.zone_type_id == type_id))
        return result.scalars().all()