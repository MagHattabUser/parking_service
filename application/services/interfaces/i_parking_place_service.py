from abc import ABC, abstractmethod
from typing import List

from web.schemas import ParkingPlaceCreate, ParkingPlaceResponse

class IParkingPlaceService(ABC):
    @abstractmethod
    async def create_place(self, data: ParkingPlaceCreate) -> ParkingPlaceResponse:
        pass

    @abstractmethod
    async def get_place(self, place_id: int) -> ParkingPlaceResponse:
        pass

    @abstractmethod
    async def list_by_zone(self, zone_id: int) -> List[ParkingPlaceResponse]:
        pass

    @abstractmethod
    async def list_by_status(self, status_id: int) -> List[ParkingPlaceResponse]:
        pass

    @abstractmethod
    async def delete_place(self, place_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_places(self) -> List[ParkingPlaceResponse]:
        pass

    @abstractmethod
    async def update_place(self, place_id: int, data: ParkingPlaceCreate) -> ParkingPlaceResponse:
        pass

    @abstractmethod
    async def update_place_status(self, place_id: int, status_id: int) -> ParkingPlaceResponse:
        pass