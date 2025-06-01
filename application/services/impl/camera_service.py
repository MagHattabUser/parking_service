from typing import List, Dict
from web.schemas import CameraCreate, CameraResponse
from application.services.interfaces.i_camera_service import ICameraService
from infrastructure.repositories.camera import CameraRepository
from web.mapper import CameraMapper
from domain.models import Camera
from infrastructure.utils.s3_utils import get_image_from_minio

class CameraService(ICameraService):
    async def list_by_zone(self, zone_id: int) -> List[CameraResponse]:
        cameras = await self.camera_repo.list_by_zone(zone_id)
        return [self.mapper.to_response(camera) for camera in cameras]

    def __init__(self, camera_repo: CameraRepository):
        self.camera_repo = camera_repo
        self.mapper = CameraMapper()

    async def create_camera(self, data: CameraCreate) -> CameraResponse:
        camera = self.mapper.to_entity(data)
        created_camera = await self.camera_repo.save(camera)
        return self.mapper.to_response(created_camera)

    async def get_camera(self, camera_id: int) -> CameraResponse:
        camera = await self.camera_repo.get_by_id(Camera, camera_id)
        if not camera:
            raise ValueError(f"Camera with id {camera_id} not found")
        return self.mapper.to_response(camera)

    async def get_all_cameras(self) -> List[CameraResponse]:
        cameras = await self.camera_repo.get_by_all(Camera)
        return [self.mapper.to_response(camera) for camera in cameras]

    async def update_camera(self, camera_id: int, data: CameraCreate) -> CameraResponse:
        camera = await self.camera_repo.get_by_id(Camera, camera_id)
        if not camera:
            raise ValueError(f"Camera with id {camera_id} not found")
        
        updated_camera = self.mapper.to_entity(data)
        updated_camera.id = camera_id
        
        updated_camera = await self.camera_repo.update(updated_camera)
        return self.mapper.to_response(updated_camera)

    async def delete_camera(self, camera_id: int) -> None:
        camera = await self.camera_repo.get_by_id(Camera, camera_id)
        if not camera:
            raise ValueError(f"Camera with id {camera_id} not found")
        await self.camera_repo.delete(camera)

    async def get_zone_snapshots(self, zone_id: int) -> Dict[int, bytes]:
        cameras = await self.camera_repo.list_by_zone(zone_id)
        if not cameras:
            raise ValueError(f"No cameras found for zone {zone_id}")
        
        snapshots = {}
        for camera in cameras:
            # В реальном приложении здесь будет запрос к камере
            # Сейчас просто получаем тестовое изображение из MinIO
            image_data = get_image_from_minio("images/test.jpg")
            snapshots[camera.id] = image_data
            
        return snapshots 