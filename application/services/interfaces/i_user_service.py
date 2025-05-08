from abc import ABC, abstractmethod
from typing import List

from web.schemas import UserCreate, UserResponse

class IUserService(ABC):
    @abstractmethod
    async def create_user(self, data: UserCreate) -> UserResponse:
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> UserResponse:
        pass

    @abstractmethod
    async def get_all_users(self) -> List[UserResponse]:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, data: UserCreate) -> UserResponse:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        pass