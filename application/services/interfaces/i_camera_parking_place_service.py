from abc import ABC, abstractmethod
from typing import List

from web.schemas import CameraParkingPlaceCreate, CameraParkingPlaceResponse

class ICameraParkingPlaceService(ABC):
    @abstractmethod
    async def create_link(self, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        pass

    @abstractmethod
    async def list_places_for_camera(self, camera_id: int) -> List[CameraParkingPlaceResponse]:
        pass

    @abstractmethod
    async def list_cameras_for_place(self, place_id: int) -> List[CameraParkingPlaceResponse]:
        pass

    @abstractmethod
    def _validate_polygon(self, coordinates: List[List[float]]) -> None:
        pass

    @abstractmethod
    async def create_camera_parking_place(self, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        pass

    @abstractmethod
    async def get_camera_parking_place(self, camera_parking_place_id: int) -> CameraParkingPlaceResponse:
        pass

    @abstractmethod
    async def get_all_camera_parking_places(self) -> List[CameraParkingPlaceResponse]:
        pass

    @abstractmethod
    async def update_camera_parking_place(self, camera_parking_place_id: int,
                                          data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        pass

    @abstractmethod
    async def delete_camera_parking_place(self, camera_parking_place_id: int) -> None:
        pass

    @abstractmethod
    async def get_marked_zone_image(self, zone_id: int) -> dict:
        pass