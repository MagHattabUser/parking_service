from typing import Optional
from domain.models import Car
from domain.i_base import IBase
from abc import abstractmethod

class ICar(IBase):
    @abstractmethod
    async def get_by_number(self, car_number: str) -> Optional[Car]:
        pass