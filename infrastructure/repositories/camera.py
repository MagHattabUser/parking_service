from sqlalchemy.future import select

from domain.i_camera import ICamera
from infrastructure.repositories.base import BaseRepository
from domain.models import Camera

class CameraRepository(BaseRepository, ICamera):
    async def list_by_zone(self, zone_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(Camera).where(Camera.parking_zone_id == zone_id))
        return result.scalars().all()