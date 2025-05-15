from typing import Optional
from domain.models import User
from domain.i_base import IBase
from abc import abstractmethod

class IUser(IBase):
    @abstractmethod
    async def get_by_phone(self, phone: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass