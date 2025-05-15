from abc import ABC, abstractmethod
from typing import Optional, Union, Any

from domain.models import User, Admin


class IUnifiedAuth(ABC):
    @abstractmethod
    async def verify_credentials(self, email: str, password: str, role: str) -> Optional[Union[User, Admin]]:
        pass

    @abstractmethod
    async def save_refresh_token(self, subject_id: int, role: str, token: str = None) -> str:
        pass

    @abstractmethod
    async def get_refresh_token(self, subject_id: int, role: str) -> Optional[str]:
        pass
    
    @abstractmethod
    async def validate_refresh_token(self, subject_id: int, role: str, token: str) -> bool:
        pass
    
    @abstractmethod
    async def invalidate_refresh_token(self, subject_id: int, role: str) -> None:
        pass
