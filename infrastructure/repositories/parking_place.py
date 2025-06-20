from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime

from domain.i_parking_place import IParkingPlace
from infrastructure.repositories.base import BaseRepository
from domain.models import ParkingPlace, Booking

class ParkingPlaceRepository(IParkingPlace):
    async def list_by_zone(self, zone_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingPlace).where(ParkingPlace.parking_zone_id == zone_id))
        return result.scalars().all()

    async def list_by_status(self, status_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(ParkingPlace).where(ParkingPlace.place_status_id == status_id))
        return result.scalars().all()

    async def free_up_expired_booking_places(self) -> None:
        now = datetime.utcnow()
        async with self.db.get_session() as session:
            subquery = select(Booking.parking_place_id).where(
                Booking.end_time < now,
                Booking.booking_status_id == 1
            ).subquery()

            stmt = update(ParkingPlace).where(
                ParkingPlace.id.in_(select(subquery)),
                ParkingPlace.place_status_id == 2
            ).values(place_status_id=1)
            
            await session.execute(stmt)
            await session.commit()

    async def occupy_started_booking_places(self) -> None:
        now = datetime.utcnow()
        async with self.db.get_session() as session:
            subquery = select(Booking.parking_place_id).where(
                Booking.start_time <= now,
                Booking.end_time >= now,
                Booking.booking_status_id == 1
            ).subquery()

            stmt = update(ParkingPlace).where(
                ParkingPlace.id.in_(select(subquery)),
                ParkingPlace.place_status_id == 1
            ).values(place_status_id=2)
            
            await session.execute(stmt)
            await session.commit()