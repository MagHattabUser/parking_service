from abc import ABC, abstractmethod
from typing import List

from web.schemas import CarUserCreate, CarUserResponse, CarUserDetailedResponse

class ICarUserService(ABC):
    @abstractmethod
    async def get_detailed_by_user(self, user_id: int) -> List[CarUserDetailedResponse]:
        pass
        
    @abstractmethod
    async def assign_car(self, data: CarUserCreate) -> CarUserResponse:
        pass

    @abstractmethod
    async def unassign_car(self, car_user_id: int) -> None:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: int) -> List[CarUserResponse]:
        pass

    @abstractmethod
    async def list_by_car(self, car_id: int) -> List[CarUserResponse]:
        pass

    @abstractmethod
    async def create_car_user(self, data: CarUserCreate) -> CarUserResponse:
        pass

    @abstractmethod
    async def get_car_user(self, car_user_id: int) -> CarUserResponse:
        pass

    @abstractmethod
    async def get_all_car_users(self) -> List[CarUserResponse]:
        pass

    @abstractmethod
    async def update_car_user(self, car_user_id: int, data: CarUserCreate) -> CarUserResponse:
        pass

    @abstractmethod
    async def delete_car_user(self, car_user_id: int) -> None:
        pass