from typing import List
from datetime import datetime, timedelta
from web.schemas import BookingCreate, BookingResponse, ParkingPlaceCreate, BookingDetailedResponse, BookingCreateWithoutEnd, BookingFinishResponse
from application.services.interfaces.i_booking_service import IBookingService
from application.services.interfaces.i_parking_place_service import IParkingPlaceService
from infrastructure.repositories.booking import BookingRepository
from web.mapper import BookingMapper
from domain.models import Booking

class BookingService(IBookingService):
    def __init__(self, booking_repo: BookingRepository, parking_place_service: IParkingPlaceService):
        self.booking_repo = booking_repo
        self.parking_place_service = parking_place_service
        self.mapper = BookingMapper()

    async def list_active_bookings(self) -> List[BookingResponse]:
        bookings = await self.booking_repo.list_active()
        return [self.mapper.to_response(booking) for booking in bookings]
        
    async def get_active_bookings(self, current_time: datetime) -> List[BookingResponse]:
        """
        Получает список активных бронирований на указанный момент времени.
        Активным считается бронирование, если current_time находится между start_time и end_time,
        либо если время окончания не установлено, а время начала уже прошло.
        """
        bookings = await self.booking_repo.get_by_all(Booking)
        active_bookings = []
        for booking in bookings:
            if booking.booking_status_id == 1:  # Предполагаем, что статус "активно" имеет id = 1
                # Убедимся, что current_time наивный для сравнения
                naive_current_time = current_time.replace(tzinfo=None)
                if booking.end_time is not None:
                    if booking.start_time <= naive_current_time <= booking.end_time:
                        active_bookings.append(booking)
                else:  # end_time is None
                    if booking.start_time <= naive_current_time:
                        active_bookings.append(booking)
        
        return [self.mapper.to_response(booking) for booking in active_bookings]

    async def list_by_user(self, user_id: int) -> List[BookingResponse]:
        bookings = await self.booking_repo.list_by_user(user_id)
        return [self.mapper.to_response(booking) for booking in bookings]

    async def list_by_status(self, status_id: int) -> List[BookingResponse]:
        bookings = await self.booking_repo.list_by_status(status_id)
        return [self.mapper.to_response(booking) for booking in bookings]

    async def create_booking(self, data: BookingCreate) -> BookingResponse:
        # 1. Проверяем на пересечение с существующими бронированиями
        if await self.booking_repo.has_overlapping_booking(
            data.parking_place_id, data.start_time, data.end_time
        ):
            raise ValueError("Выбранное время для бронирования уже занято.")

        # 2. Создаем бронирование
        booking = self.mapper.to_entity(data)
        created_booking = await self.booking_repo.save(booking)

        # 3. Обновляем статус места на "занято", только если бронь начинается сейчас
        now = datetime.utcnow()
        if created_booking.start_time <= now:
            await self.parking_place_service.update_place_status(data.parking_place_id, 2)  # 2 - занято

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
        
    async def get_detailed_by_user(self, user_id: int) -> List[BookingDetailedResponse]:
        """
        Получение детальной информации по всем бронированиям пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Список объектов BookingDetailedResponse с детальной информацией о бронированиях
        """
        booking_details = await self.booking_repo.get_detailed_by_user(user_id)
        
        result = []
        for booking, place_number, address, zone_name, booking_status_name, car_number in booking_details:
            result.append(
                BookingDetailedResponse(
                    id=booking.id,
                    address=address,
                    zone_name=zone_name,
                    place_number=place_number,
                    start_time=booking.start_time,
                    end_time=booking.end_time,
                    car_number=car_number,
                    booking_status_name=booking_status_name
                )
            )
            
        return result
        
    async def create_booking_without_end(self, data: BookingCreateWithoutEnd) -> BookingResponse:
        """
        Создание бронирования без указания времени окончания
        
        Args:
            data: Данные для создания бронирования
            
        Returns:
            Объект BookingResponse с информацией о созданном бронировании
        """
        # Проверяем доступность места
        place = await self.parking_place_service.get_place(data.parking_place_id)
        if place.place_status_id == 2:  # 2 - Занято
            raise ValueError(f"Parking place {data.parking_place_id} is already occupied")
        
        # Создаем объект бронирования с текущим временем начала и без конца
        current_time = datetime.utcnow()
        
        booking = Booking(
            car_user_id=data.car_user_id,
            start_time=current_time,
            end_time=None,  # Время окончания не указано
            parking_place_id=data.parking_place_id,
            booking_status_id=data.booking_status_id
        )
        
        # Сохраняем бронирование
        created_booking = await self.booking_repo.save(booking)
        
        # Обновляем статус места на 'Занято'
        await self.parking_place_service.update_place_status(data.parking_place_id, 2)
        
        return BookingResponse(
            id=created_booking.id,
            car_user_id=created_booking.car_user_id,
            start_time=created_booking.start_time,
            end_time=created_booking.end_time,
            parking_place_id=created_booking.parking_place_id,
            booking_status_id=created_booking.booking_status_id
        )
        
    async def finish_booking(self, booking_id: int) -> BookingFinishResponse:
        """
        Завершение бронирования с расчетом стоимости
        
        Args:
            booking_id: ID бронирования для завершения
            
        Returns:
            Объект BookingFinishResponse с информацией о стоимости
        """
        # Получаем бронирование
        booking = await self.booking_repo.get_by_id(Booking, booking_id)
        if not booking:
            raise ValueError(f"Booking with id {booking_id} not found")
        
        # Проверяем, не завершено ли уже бронирование
        if booking.end_time is not None:
            raise ValueError(f"Booking with id {booking_id} is already finished")
        
        # Получаем информацию о парковочном месте и зоне для расчета стоимости
        place = await self.parking_place_service.get_place(booking.parking_place_id)
        
        # Обновляем бронирование - устанавливаем время окончания и меняем статус
        current_time = datetime.utcnow()
        booking.end_time = current_time
        booking.booking_status_id = 2  # Завершено
        
        # Сохраняем обновленное бронирование
        await self.booking_repo.update(booking)
        
        # Освобождаем парковочное место
        await self.parking_place_service.update_place_status(booking.parking_place_id, 1)  # 1 - Свободно
        
        # Получаем информацию о зоне для определения цены за минуту
        zone = await self.booking_repo.get_zone_by_place_id(booking.parking_place_id)
        
        # Рассчитываем длительность в минутах и стоимость
        duration_seconds = (current_time - booking.start_time).total_seconds()
        duration_minutes = int(duration_seconds / 60)
        if duration_minutes < 1:  # Минимальная оплата за 1 минуту
            duration_minutes = 1
            
        total_price = zone.price_per_minute * duration_minutes
        
        return BookingFinishResponse(
            id=booking.id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            duration_minutes=duration_minutes,
            price_per_minute=zone.price_per_minute,
            total_price=total_price,
            status="Завершено"
        )

    async def complete_expired_bookings(self) -> None:
        await self.booking_repo.complete_expired_bookings()