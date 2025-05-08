from abc import ABC, abstractmethod
from typing import List

from web.schemas import AdminCreate, AdminResponse

class IAdminService(ABC):
    @abstractmethod
    async def create_admin(self, data: AdminCreate) -> AdminResponse:
        pass

    @abstractmethod
    async def get_admin(self, admin_id: int) -> AdminResponse:
        pass

    @abstractmethod
    async def get_all_admins(self) -> List[AdminResponse]:
        pass

    @abstractmethod
    async def update_admin(self, admin_id: int, data: AdminCreate) -> AdminResponse:
        pass

    @abstractmethod
    async def delete_admin(self, admin_id: int) -> None:
        pass