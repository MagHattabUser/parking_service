from typing import List
from web.schemas import BookingStatusCreate, BookingStatusResponse
from application.services.interfaces.i_booking_status_service import IBookingStatusService
from infrastructure.repositories.booking_status import BookingStatusRepository
from web.mapper import BookingStatusMapper
from domain.models import BookingStatus

class BookingStatusService(IBookingStatusService):
    def __init__(self, booking_status_repo: BookingStatusRepository):
        self.booking_status_repo = booking_status_repo
        self.mapper = BookingStatusMapper()

    async def list_all_statuses(self) -> List[BookingStatusResponse]:
        statuses = await self.booking_status_repo.get_by_all(BookingStatus)
        return [self.mapper.to_response(status) for status in statuses]

    async def create_booking_status(self, data: BookingStatusCreate) -> BookingStatusResponse:
        booking_status = self.mapper.to_entity(data)
        created_booking_status = await self.booking_status_repo.save(booking_status)
        return self.mapper.to_response(created_booking_status)

    async def get_booking_status(self, booking_status_id: int) -> BookingStatusResponse:
        booking_status = await self.booking_status_repo.get_by_id(BookingStatus, booking_status_id)
        if not booking_status:
            raise ValueError(f"BookingStatus with id {booking_status_id} not found")
        return self.mapper.to_response(booking_status)

    async def update_booking_status(self, booking_status_id: int, data: BookingStatusCreate) -> BookingStatusResponse:
        booking_status = await self.booking_status_repo.get_by_id(BookingStatus, booking_status_id)
        if not booking_status:
            raise ValueError(f"BookingStatus with id {booking_status_id} not found")
        
        updated_booking_status = self.mapper.to_entity(data)
        updated_booking_status.id = booking_status_id
        
        updated_booking_status = await self.booking_status_repo.update(updated_booking_status)
        return self.mapper.to_response(updated_booking_status)

    async def delete_booking_status(self, booking_status_id: int) -> None:
        booking_status = await self.booking_status_repo.get_by_id(BookingStatus, booking_status_id)
        if not booking_status:
            raise ValueError(f"BookingStatus with id {booking_status_id} not found")
        await self.booking_status_repo.delete(booking_status) 