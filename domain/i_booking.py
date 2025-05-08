from typing import List, Optional
from domain.models import Booking
from domain.i_base import IBase
from abc import abstractmethod

class IBooking(IBase):
    @abstractmethod
    async def list_by_user(self, user_id: int) -> List[Booking]:
        """История бронирований конкретного пользователя"""
        pass

    @abstractmethod
    async def list_active(self) -> List[Booking]:
        """Все активные (текущие) бронирования"""
        pass

    @abstractmethod
    async def list_by_status(self, status_id: int) -> List[Booking]:
        """Фильтрация бронирований по статусу"""
        pass