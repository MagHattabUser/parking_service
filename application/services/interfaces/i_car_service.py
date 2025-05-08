from abc import ABC, abstractmethod
from typing import List

from web.schemas import CarCreate, CarResponse

class ICarService(ABC):
    @abstractmethod
    async def create_car(self, data: CarCreate) -> CarResponse:
        pass

    @abstractmethod
    async def get_car(self, car_id: int) -> CarResponse:
        pass

    @abstractmethod
    async def get_all_cars(self) -> List[CarResponse]:
        pass

    @abstractmethod
    async def update_car(self, car_id: int, data: CarCreate) -> CarResponse:
        pass

    @abstractmethod
    async def delete_car(self, car_id: int) -> None:
        pass