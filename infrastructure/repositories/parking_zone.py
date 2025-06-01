from typing import List, Tuple, Dict

from sqlalchemy.future import select
from sqlalchemy import and_, func, update
from sqlalchemy.orm import joinedload

from domain.i_parking_zone import IParkingZone
from infrastructure.repositories.base import BaseRepository
from domain.models import ParkingZone, ParkingPlace, Camera, ZoneType, PlaceStatus, CameraParkingPlace

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
            
    async def get_places_by_zone(self, zone_id: int) -> List[Tuple[ParkingPlace, Dict]]:
        """Получить все парковочные места в зоне с их координатами"""
        async with self.db.get_session() as session:
            # Получаем все места в зоне
            places_query = select(ParkingPlace).where(ParkingPlace.parking_zone_id == zone_id)
            places_result = await session.execute(places_query)
            parking_places = places_result.scalars().all()
            
            result = []
            
            # Для каждого места находим его координаты в таблице CameraParkingPlace
            for place in parking_places:
                camera_place_query = select(CameraParkingPlace).where(
                    CameraParkingPlace.parking_place_id == place.id
                )
                camera_place_result = await session.execute(camera_place_query)
                camera_place = camera_place_result.scalars().first()
                
                # Если есть связь с камерой, используем координаты из нее
                location = None
                if camera_place:
                    location = camera_place.location
                
                result.append((place, {"location": location}))
                
            return result
    
    async def update_places_status(self, place_status_updates: Dict[int, int]) -> int:
        """Обновить статусы парковочных мест"""
        if not place_status_updates:
            return 0
            
        updated_count = 0
        async with self.db.get_session() as session:
            for place_id, status_id in place_status_updates.items():
                # Получаем место по ID
                place_query = select(ParkingPlace).where(ParkingPlace.id == place_id)
                place_result = await session.execute(place_query)
                place = place_result.scalars().first()
                
                if place:
                    # Обновляем статус
                    place.place_status_id = status_id
                    session.add(place)
                    updated_count += 1
            
            # Сохраняем изменения
            await session.commit()
            
        return updated_count