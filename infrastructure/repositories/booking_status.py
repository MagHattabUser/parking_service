from typing import List

from sqlalchemy.future import select

from domain.i_booking_status import IBookingStatus
from infrastructure.repositories.base import BaseRepository
from domain.models import BookingStatus

class BookingStatusRepository(BaseRepository, IBookingStatus):
    pass

