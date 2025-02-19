from functools import lru_cache

import punq

from infrastructure.database import Database
from infrastructure.repositories.parking_zone import ParkingZoneRepository
from infrastructure.repositories.parking_place import ParkingPlaceRepository
from domain.i_parking_place import IParkingPlace
from domain.i_parking_zone import IParkingZone
from application.services.i_place_service import IPlaceService
from application.services.i_zone_service import IZoneService
from application.services.impl.zone_service import ZoneService
from application.services.impl.place_service import PlaceService
from web.config import Configs


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()

def _init_container() -> punq.Container:
    container = punq.Container()

    container.register(
        Configs,
        scope=punq.Scope.singleton,
        instance=Configs()
    )
    configs: Configs = container.resolve(Configs)
    container.register(
        Database,
        scope=punq.Scope.singleton,
        factory=lambda: Database(
            url=configs.DATABASE_URL,
        ),
    )
    container.register(IParkingZone, factory=lambda: ParkingZoneRepository(container.resolve(Database)))
    container.register(IParkingPlace, factory=lambda: ParkingPlaceRepository(container.resolve(Database)))

    container.register(IZoneService, factory=lambda: ZoneService(container.resolve(IParkingZone)))
    container.register(IPlaceService, factory=lambda: PlaceService(container.resolve(IParkingPlace)))
    return container
