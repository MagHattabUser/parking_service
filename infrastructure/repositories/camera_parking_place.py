from sqlalchemy.future import select

from domain.i_camera_parking_place import ICameraParkingPlace
from infrastructure.repositories.base import BaseRepository
from domain.models import CameraParkingPlace, Camera

class CameraParkingPlaceRepository(BaseRepository, ICameraParkingPlace):
    async def list_places_by_camera(self, camera_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(CameraParkingPlace).where(CameraParkingPlace.camera_id == camera_id))
        return result.scalars().all()

    async def list_cameras_by_place(self, place_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(CameraParkingPlace).where(CameraParkingPlace.parking_place_id == place_id))
        return result.scalars().all()

    async def list_places_by_zone(self, zone_id: int):
        async with self.db.get_session() as session:
            # Use selectinload to eagerly load the parking_place relationship
            from sqlalchemy.orm import selectinload
            result = await session.execute(
                select(CameraParkingPlace)
                .join(CameraParkingPlace.camera)
                .options(selectinload(CameraParkingPlace.parking_place))
                .where(CameraParkingPlace.camera.has(Camera.parking_zone_id == zone_id))
            )
            # Make sure to materialize the results before closing the session
            places = result.scalars().all()
        return places