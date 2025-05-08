from abc import ABC, abstractmethod
from typing import List

from web.schemas import BookingCreate, BookingResponse

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