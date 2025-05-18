from typing import List, Tuple

from sqlalchemy.future import select
from sqlalchemy import and_, func

from domain.i_parking_zone import IParkingZone
from infrastructure.repositories.base import BaseRepository
from domain.models import ParkingZone, ParkingPlace, Camera, ZoneType, PlaceStatus

class ParkingZoneRepository(BaseRepository, IParkingZone):
    async def list_by_admin(self, admin_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingZone).where(ParkingZone.admin_id == admin_id))
        return result.scalars().all()

    async def list_by_type(self, type_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingZone).where(ParkingZone.zone_type_id == type_id))
        return result.scalars().all()

    async def get_zone_detailed(self, zone_id: int) -> Tuple[ParkingZone, ZoneType, int, int, int, int]:
        async with self.db.get_session() as session:
            zone_query = select(ParkingZone, ZoneType).join(
                ZoneType, ParkingZone.zone_type_id == ZoneType.id
            ).where(ParkingZone.id == zone_id)
            zone_result = await session.execute(zone_query)
            zone_data = zone_result.first()
            
            if not zone_data:
                return None

            zone, zone_type = zone_data

            places_query = select(func.count(ParkingPlace.id)).where(ParkingPlace.parking_zone_id == zone_id)
            total_places = await session.execute(places_query)
            total_places = total_places.scalar() or 0

            free_places_query = select(func.count(ParkingPlace.id)).join(
                PlaceStatus, ParkingPlace.place_status_id == PlaceStatus.id
            ).where(
                and_(
                    ParkingPlace.parking_zone_id == zone_id,
                    PlaceStatus.status_name == "Свободно"
                )
            )
            free_places = await session.execute(free_places_query)
            free_places = free_places.scalar() or 0

            occupied_places_query = select(func.count(ParkingPlace.id)).join(
                PlaceStatus, ParkingPlace.place_status_id == PlaceStatus.id
            ).where(
                and_(
                    ParkingPlace.parking_zone_id == zone_id,
                    PlaceStatus.status_name == "Занято"
                )
            )
            occupied_places = await session.execute(occupied_places_query)
            occupied_places = occupied_places.scalar() or 0

            cameras_query = select(func.count(Camera.id)).where(Camera.parking_zone_id == zone_id)
            total_cameras = await session.execute(cameras_query)
            total_cameras = total_cameras.scalar() or 0

            return zone, zone_type, total_places, free_places, occupied_places, total_cameras