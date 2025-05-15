from typing import List, Optional
from domain.models import CameraParkingPlace
from domain.i_base import IBase
from abc import abstractmethod

class ICameraParkingPlace(IBase):
    @abstractmethod
    async def list_places_by_camera(self, camera_id: int) -> List[CameraParkingPlace]:
        pass

    @abstractmethod
    async def list_cameras_by_place(self, place_id: int) -> List[CameraParkingPlace]:
        pass