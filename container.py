from functools import lru_cache

import punq

from database import Database
from repositories.impl.parking_zone import ParkingZoneRepository
from repositories.impl.parking_place import ParkingPlaceRepository
from repositories.i_parking_place import IParkingPlace
from repositories.i_parking_zone import IParkingZone
from services.zone_service import ZoneService
from services.place_service import PlaceService
from config import Configs


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
            url=configs.SQLite_CONNECTION_URI,
        ),
    )
    container.register(IParkingZone, factory=lambda: ParkingZoneRepository(container.resolve(Database)))
    container.register(IParkingPlace, factory=lambda: ParkingPlaceRepository(container.resolve(Database)))

    container.register(ZoneService, factory=lambda: ZoneService(container.resolve(IParkingZone)))
    container.register(PlaceService, factory=lambda: PlaceService(container.resolve(IParkingPlace)))
    return container
