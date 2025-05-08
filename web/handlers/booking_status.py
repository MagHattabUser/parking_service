from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import BookingStatusCreate, BookingStatusResponse
from application.services.interfaces.i_booking_status_service import IBookingStatusService

router = APIRouter(prefix="/booking-status", tags=["booking-status"])

def get_booking_status_service() -> IBookingStatusService:
    return get_container().resolve(IBookingStatusService)

@router.post("/", response_model=BookingStatusResponse)
async def create_booking_status(data: BookingStatusCreate, service: IBookingStatusService = Depends(get_booking_status_service)):
    return await service.create_booking_status(data)

@router.get("/{status_id}", response_model=BookingStatusResponse)
async def get_booking_status(status_id: int, service: IBookingStatusService = Depends(get_booking_status_service)):
    return await service.get_booking_status(status_id)

@router.get("/", response_model=List[BookingStatusResponse])
async def get_all_booking_statuses(service: IBookingStatusService = Depends(get_booking_status_service)):
    return await service.list_all_statuses()

@router.put("/{status_id}", response_model=BookingStatusResponse)
async def update_booking_status(status_id: int, data: BookingStatusCreate, service: IBookingStatusService = Depends(get_booking_status_service)):
    return await service.update_booking_status(status_id, data)

@router.delete("/{status_id}")
async def delete_booking_status(status_id: int, service: IBookingStatusService = Depends(get_booking_status_service)):
    await service.delete_booking_status(status_id)
    return {"message": "Booking status deleted successfully"} 