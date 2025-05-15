from typing import Optional
from domain.models import Admin
from domain.i_base import IBase
from abc import abstractmethod

class IAdmin(IBase):
    @abstractmethod
    async def get_by_name(self, admin_name: str) -> Optional[Admin]:
        pass