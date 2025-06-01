from abc import ABC, abstractmethod
from typing import List, Dict

from web.schemas import CameraCreate, CameraResponse

class ICameraService(ABC):
    @abstractmethod
    async def create_camera(self, data: CameraCreate) -> CameraResponse:
        pass

    @abstractmethod
    async def get_camera(self, camera_id: int) -> CameraResponse:
        pass

    @abstractmethod
    async def list_by_zone(self, zone_id: int) -> List[CameraResponse]:
        pass

    @abstractmethod
    async def delete_camera(self, camera_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_cameras(self) -> List[CameraResponse]:
        pass

    @abstractmethod
    async def update_camera(self, camera_id: int, data: CameraCreate) -> CameraResponse:
        pass

    @abstractmethod
    async def get_zone_snapshots(self, zone_id: int) -> Dict[int, bytes]:
        pass