from typing import List, Optional
from domain.models import CarUser
from domain.i_base import IBase
from abc import abstractmethod

class ICarUser(IBase):
    @abstractmethod
    async def list_by_user(self, user_id: int) -> List[CarUser]:
        pass

    @abstractmethod
    async def list_by_car(self, car_id: int) -> List[CarUser]:
        pass