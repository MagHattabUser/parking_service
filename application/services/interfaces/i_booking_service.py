from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

from web.schemas import BookingCreate, BookingResponse, BookingDetailedResponse, BookingCreateWithoutEnd, BookingFinishResponse

class IBookingService(ABC):
    @abstractmethod
    async def create_booking(self, data: BookingCreate) -> BookingResponse:
        pass

    @abstractmethod
    async def get_booking(self, booking_id: int) -> BookingResponse:
        pass

    @abstractmethod
    async def get_all_bookings(self) -> List[BookingResponse]:
        pass

    @abstractmethod
    async def list_active_bookings(self) -> List[BookingResponse]:
        pass
        
    @abstractmethod
    async def get_active_bookings(self, current_time: datetime) -> List[BookingResponse]:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: int) -> List[BookingResponse]:
        pass

    @abstractmethod
    async def list_by_status(self, status_id: int) -> List[BookingResponse]:
        pass

    @abstractmethod
    async def update_booking(self, booking_id: int, data: BookingCreate) -> BookingResponse:
        pass

    @abstractmethod
    async def delete_booking(self, booking_id: int) -> None:
        pass
        
    @abstractmethod
    async def get_detailed_by_user(self, user_id: int) -> List[BookingDetailedResponse]:
        pass
        
    @abstractmethod
    async def create_booking_without_end(self, data: BookingCreateWithoutEnd) -> BookingResponse:
        pass
        
    @abstractmethod
    async def finish_booking(self, booking_id: int) -> BookingFinishResponse:
        pass