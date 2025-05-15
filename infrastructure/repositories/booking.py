from sqlalchemy.future import select
from datetime import datetime

from domain.i_booking import IBooking
from infrastructure.repositories.base import BaseRepository
from domain.models import Booking, CarUser

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