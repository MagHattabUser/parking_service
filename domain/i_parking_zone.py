from typing import List, Optional
from domain.models import ParkingZone
from domain.i_base import IBase
from abc import abstractmethod

class IParkingZone(IBase):
    @abstractmethod
    async def list_by_admin(self, admin_id: int) -> List[ParkingZone]:
        """Все зоны, администрируемые конкретным администратором"""
        pass

    @abstractmethod
    async def list_by_type(self, type_id: int) -> List[ParkingZone]:
        """Фильтрация зон по их типу"""
        pass