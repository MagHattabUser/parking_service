from sqlalchemy.future import select

from domain.i_camera_parking_place import ICameraParkingPlace
from infrastructure.repositories.base import BaseRepository
from domain.models import CameraParkingPlace

class CameraParkingPlaceRepository(BaseRepository, ICameraParkingPlace):
    async def list_places_by_camera(self, camera_id: int):
        """Все CameraParkingPlace для конкретной камеры"""
        async with self.db.get_session() as session:
            result = await session.execute(select(CameraParkingPlace).where(CameraParkingPlace.camera_id == camera_id))
        return result.scalars().all()

    async def list_cameras_by_place(self, place_id: int):
        """Все CameraParkingPlace для конкретного места"""
        async with self.db.get_session() as session:
            result = await session.execute(select(CameraParkingPlace).where(CameraParkingPlace.parking_place_id == place_id))
        return result.scalars().all()