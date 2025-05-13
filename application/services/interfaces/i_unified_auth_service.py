from abc import ABC, abstractmethod
from typing import Optional, Union, Any

from domain.models import User, Admin
from web.schemas import Token, UserCreate, AdminCreate


class IUnifiedAuthService(ABC):
    @abstractmethod
    async def register(self, data: Union[UserCreate, AdminCreate], role: str) -> Union[User, Admin]:
        pass
        
    @abstractmethod
    async def authenticate(self, email: str, password: str, role: str) -> Optional[Union[User, Admin]]:
        pass
    
    @abstractmethod
    async def create_token(self, subject: Union[User, Admin], role: str) -> Token:
        pass

    @abstractmethod
    async def get_by_email(self, email: str, role: str) -> Optional[Union[User, Admin]]:
        pass
        
    @abstractmethod
    async def logout(self, subject_id: int, role: str) -> None:
        pass
        
    @abstractmethod
    async def refresh_access_token(self, subject_id: int, role: str, refresh_token: str) -> Optional[Token]:
        pass
