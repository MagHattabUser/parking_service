from typing import List, Optional
from domain.models import Camera
from domain.i_base import IBase
from abc import abstractmethod

class ICamera(IBase):
    @abstractmethod
    async def list_by_zone(self, zone_id: int) -> List[Camera]:
        pass