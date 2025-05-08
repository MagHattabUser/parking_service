from typing import List

from sqlalchemy.future import select

from domain.i_zone_type import IZoneType
from infrastructure.repositories.base import BaseRepository
from domain.models import ZoneType

class ZoneTypeRepository(BaseRepository, IZoneType):
    pass

