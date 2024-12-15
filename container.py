from functools import lru_cache

import punq
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import ParkingZone, ParkingPlace
from repositories.parking_zone import ParkingZoneRepository
from repositories.parking_place import ParkingPlaceRepository
from services.zone_service import ZoneService
from services.place_service import PlaceService


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    container.register(AsyncSession, factory=lambda: next(get_db()))

    container.register(ParkingZoneRepository, factory=lambda: ParkingZoneRepository(container.resolve(AsyncSession)))
    container.register(ParkingPlaceRepository, factory=lambda: ParkingPlaceRepository(container.resolve(AsyncSession)))

    container.register(ZoneService, factory=lambda: ZoneService(container.resolve(ParkingZoneRepository)))
    container.register(PlaceService, factory=lambda: PlaceService(container.resolve(ParkingPlaceRepository)))

    return container
