from abc import ABC, abstractmethod
from typing import List

from web.schemas import BookingStatusResponse, BookingStatusCreate


class IBookingStatusService(ABC):
    @abstractmethod
    async def list_all_statuses(self) -> List[BookingStatusResponse]:
        pass

    @abstractmethod
    async def create_booking_status(self, data: BookingStatusCreate) -> BookingStatusResponse:
        pass

    @abstractmethod
    async def get_booking_status(self, booking_status_id: int) -> BookingStatusResponse:
        pass

    @abstractmethod
    async def update_booking_status(self, booking_status_id: int, data: BookingStatusCreate) -> BookingStatusResponse:
        pass

    @abstractmethod
    async def delete_booking_status(self, booking_status_id: int) -> None:
        pass