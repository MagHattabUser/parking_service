from abc import ABC, abstractmethod

from web.schemas import ParkingPlaceCreate


class IPlaceService(ABC):
    @abstractmethod
    async def get_places_by_zone(self, zona_identifier: str | int):
        pass

    @abstractmethod
    async def create_place(self, place_data: ParkingPlaceCreate):
        pass

    @abstractmethod
    async def delete_place(self, place_id: int):
        pass