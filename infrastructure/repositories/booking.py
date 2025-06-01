from sqlalchemy.future import select
from datetime import datetime

from domain.i_booking import IBooking
from infrastructure.repositories.base import BaseRepository
from domain.models import Booking, CarUser, ParkingPlace, ParkingZone, BookingStatus, Car

class BookingRepository(BaseRepository, IBooking):
    async def list_by_user(self, user_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(Booking).where(Booking.user_id == user_id))
        return result.scalars().all()

    async def list_by_place(self, place_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(Booking).where(Booking.parking_place_id == place_id))
        return result.scalars().all()

    async def list_by_date_range(self, start: datetime, end: datetime):
        async with self.db.get_session() as session:
            result = await session.execute(select(Booking).where(Booking.start_time.between(start, end)))
        return result.scalars().all()

    async def list_active(self):
        now = datetime.utcnow()
        async with self.db.get_session() as session:
            stmt = select(Booking).where(Booking.start_time <= now, Booking.end_time >= now)
            result = await session.execute(stmt)
        return result.scalars().all()

    async def list_by_status(self, status_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(Booking).where(Booking.booking_status_id == status_id))
        return result.scalars().all()
        
    async def get_detailed_by_user(self, user_id: int):
        """Получение детальной информации по всем бронированиям пользователя"""
        async with self.db.get_session() as session:
            # Создаем сложный запрос для получения всех необходимых данных в одной выборке
            stmt = select(
                Booking,
                ParkingPlace.place_number,
                ParkingZone.address,
                ParkingZone.zone_name,
                BookingStatus.status_name.label("booking_status_name"),
                Car.car_number
            ).join(
                CarUser, Booking.car_user_id == CarUser.id
            ).join(
                Car, CarUser.car_id == Car.id
            ).join(
                ParkingPlace, Booking.parking_place_id == ParkingPlace.id
            ).join(
                ParkingZone, ParkingPlace.parking_zone_id == ParkingZone.id
            ).join(
                BookingStatus, Booking.booking_status_id == BookingStatus.id
            ).where(
                CarUser.user_id == user_id
            )
            
            result = await session.execute(stmt)
            return result.all()
            
    async def get_zone_by_place_id(self, place_id: int):
        """Получение информации о зоне парковки по идентификатору места"""
        async with self.db.get_session() as session:
            stmt = select(ParkingZone).join(
                ParkingPlace, ParkingZone.id == ParkingPlace.parking_zone_id
            ).where(ParkingPlace.id == place_id)
            
            result = await session.execute(stmt)
            return result.scalar_one_or_none()