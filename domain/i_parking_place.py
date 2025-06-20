from typing import List, Optional
from domain.models import ParkingPlace
from domain.i_base import IBase
from infrastructure.repositories.base import BaseRepository
from abc import ABC, abstractmethod

class IParkingPlace(BaseRepository, ABC):
    @abstractmethod
    async def free_up_expired_booking_places(self) -> None:
        pass

    @abstractmethod
    async def occupy_started_booking_places(self) -> None:
        pass

    @abstractmethod
    async def list_by_zone(self, zone_id: int) -> List[ParkingPlace]:
        pass

    @abstractmethod
    async def list_by_status(self, status_id: int) -> List[ParkingPlace]:
        pass