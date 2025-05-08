from abc import ABC, abstractmethod
from typing import List, Union

from web.schemas import ParkingZoneCreate, ParkingZoneResponse

class IParkingZoneService(ABC):
    @abstractmethod
    async def create_zone(self, data: ParkingZoneCreate) -> ParkingZoneResponse:
        pass

    @abstractmethod
    async def get_zone(self, zone_id: int) -> ParkingZoneResponse:
        pass

    @abstractmethod
    async def get_all_zones(self) -> List[ParkingZoneResponse]:
        pass

    @abstractmethod
    async def update_zone(self, zone_id: int, data: ParkingZoneCreate) -> ParkingZoneResponse:
        pass

    @abstractmethod
    async def delete_zone(self, zone_id: Union[int, str]) -> None:
        pass