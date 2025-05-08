from abc import ABC, abstractmethod
from typing import List

from web.schemas import ZoneTypeResponse, ZoneTypeCreate


class IZoneTypeService(ABC):
    @abstractmethod
    async def list_all_types(self) -> List[ZoneTypeResponse]:
        pass

    @abstractmethod
    async def create_zone_type(self, data: ZoneTypeCreate) -> ZoneTypeResponse:
        pass

    @abstractmethod
    async def get_zone_type(self, zone_type_id: int) -> ZoneTypeResponse:
        pass

    @abstractmethod
    async def update_zone_type(self, zone_type_id: int, data: ZoneTypeCreate) -> ZoneTypeResponse:
        pass

    @abstractmethod
    async def delete_zone_type(self, zone_type_id: int) -> None:
        pass