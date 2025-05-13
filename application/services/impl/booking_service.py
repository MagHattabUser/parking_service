from typing import List
from web.schemas import BookingCreate, BookingResponse
from application.services.interfaces.i_booking_service import IBookingService
from infrastructure.repositories.booking import BookingRepository
from web.mapper import BookingMapper
from domain.models import Booking

class BookingService(IBookingService):
    def __init__(self, booking_repo: BookingRepository):
        self.booking_repo = booking_repo
        self.mapper = BookingMapper()

    async def list_active_bookings(self) -> List[BookingResponse]:
        bookings = await self.booking_repo.list_active()
        return [self.mapper.to_response(booking) for booking in bookings]

    async def list_by_user(self, user_id: int) -> List[BookingResponse]:
        bookings = await self.booking_repo.list_by_user(user_id)
        return [self.mapper.to_response(booking) for booking in bookings]

    async def list_by_status(self, status_id: int) -> List[BookingResponse]:
        bookings = await self.booking_repo.list_by_status(status_id)
        return [self.mapper.to_response(booking) for booking in bookings]

    async def create_booking(self, data: BookingCreate) -> BookingResponse:
        booking = self.mapper.to_entity(data)
        created_booking = await self.booking_repo.save(booking)
        return self.mapper.to_response(created_booking)

    async def get_booking(self, booking_id: int) -> BookingResponse:
        booking = await self.booking_repo.get_by_id(Booking, booking_id)
        if not booking:
            raise ValueError(f"Booking with id {booking_id} not found")
        return self.mapper.to_response(booking)

    async def get_all_bookings(self) -> List[BookingResponse]:
        bookings = await self.booking_repo.get_by_all(Booking)
        return [self.mapper.to_response(booking) for booking in bookings]

    async def update_booking(self, booking_id: int, data: BookingCreate) -> BookingResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking with id {booking_id} not found")
        
        updated_booking = self.mapper.to_entity(data)
        updated_booking.id = booking_id
        
        updated_booking = await self.booking_repo.update(updated_booking)
        return self.mapper.to_response(updated_booking)

    async def delete_booking(self, booking_id: int) -> None:
        booking = await self.booking_repo.get_by_id(Booking, booking_id)
        if not booking:
            raise ValueError(f"Booking with id {booking_id} not found")
        await self.booking_repo.delete(booking) 