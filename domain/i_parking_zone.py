from typing import List, Optional, Dict, Tuple
from domain.models import ParkingZone, ParkingPlace
from domain.i_base import IBase
from abc import abstractmethod

class IParkingZone(IBase):
    @abstractmethod
    async def list_by_admin(self, admin_id: int) -> List[ParkingZone]:
        pass

    @abstractmethod
    async def list_by_type(self, type_id: int) -> List[ParkingZone]:
        pass
        
    @abstractmethod
    async def get_places_by_zone(self, zone_id: int) -> List[Tuple[ParkingPlace, Dict]]:
        """Получить все парковочные места в зоне с их координатами"""
        pass
        
    @abstractmethod
    async def update_places_status(self, place_status_updates: Dict[int, int]) -> int:
        """Обновить статусы парковочных мест
        
        Args:
            place_status_updates: Словарь {place_id: status_id}
            
        Returns:
            Количество обновленных мест
        """
        pass