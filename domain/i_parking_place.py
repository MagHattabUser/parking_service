from typing import List, Optional
from domain.models import ParkingPlace
from domain.i_base import IBase
from abc import abstractmethod

class IParkingPlace(IBase):
    @abstractmethod
    async def list_by_zone(self, zone_id: int) -> List[ParkingPlace]:
        """Список мест в конкретной зоне"""
        pass

    @abstractmethod
    async def list_by_status(self, status_id: int) -> List[ParkingPlace]:
        """Фильтрация мест по статусу"""
        pass