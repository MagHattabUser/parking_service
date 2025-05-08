from sqlalchemy.future import select

from domain.i_place_status import IPlaceStatus
from infrastructure.repositories.base import BaseRepository
from domain.models import PlaceStatus

class PlaceStatusRepository(BaseRepository, IPlaceStatus):
    pass