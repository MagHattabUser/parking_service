from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import BookingCreate, BookingResponse
from application.services.interfaces.i_booking_service import IBookingService

router = APIRouter(prefix="/booking", tags=["booking"])

def get_booking_service() -> IBookingService:
    return get_container().resolve(IBookingService)

@router.post("/", response_model=BookingResponse)
async def create_booking(data: BookingCreate, service: IBookingService = Depends(get_booking_service)):
    return await service.create_booking(data)

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, service: IBookingService = Depends(get_booking_service)):
    return await service.get_booking(booking_id)

@router.get("/", response_model=List[BookingResponse])
async def get_all_bookings(service: IBookingService = Depends(get_booking_service)):
    return await service.get_all_bookings()

@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(booking_id: int, data: BookingCreate, service: IBookingService = Depends(get_booking_service)):
    return await service.update_booking(booking_id, data)

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, service: IBookingService = Depends(get_booking_service)):
    await service.delete_booking(booking_id)
    return {"message": "Booking deleted successfully"}

@router.get("/active/list", response_model=List[BookingResponse], summary="Список активных бронирований")
async def get_active_bookings(service: IBookingService = Depends(get_booking_service)):
    """Возвращает список всех активных бронирований"""
    return await service.list_active_bookings()

@router.get("/user/{user_id}", response_model=List[BookingResponse], summary="Бронирования пользователя")
async def get_user_bookings(user_id: int, service: IBookingService = Depends(get_booking_service)):
    """Возвращает все бронирования конкретного пользователя"""
    return await service.list_by_user(user_id)

@router.get("/status/{status_id}", response_model=List[BookingResponse], summary="Бронирования по статусу")
async def get_bookings_by_status(status_id: int, service: IBookingService = Depends(get_booking_service)):
    """Возвращает все бронирования с указанным статусом"""
    return await service.list_by_status(status_id)