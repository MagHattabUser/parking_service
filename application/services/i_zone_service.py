from abc import ABC, abstractmethod

from web.schemas import ParkingZoneCreate


class IZoneService(ABC):
    @abstractmethod
    async def create_zone(self, zone_data: ParkingZoneCreate):
        pass

    @abstractmethod
    async def get_all_zones(self):
        pass

    @abstractmethod
    async def get_zone(self, zone_id: int):
        pass

    @abstractmethod
    async def delete_zone(self, identifier: str | int):
        pass

    @abstractmethod
    async def update_zone(self, zone_id: int, zone_data: ParkingZoneCreate):
        pass