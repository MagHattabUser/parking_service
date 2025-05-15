from functools import lru_cache

import punq

from infrastructure.database import Database

from infrastructure.repositories.parking_zone import ParkingZoneRepository
from infrastructure.repositories.parking_place import ParkingPlaceRepository
from infrastructure.repositories.admin import AdminRepository
from infrastructure.repositories.booking import BookingRepository
from infrastructure.repositories.booking_status import BookingStatusRepository
from infrastructure.repositories.car import CarRepository
from infrastructure.repositories.car_user import CarUserRepository
from infrastructure.repositories.camera import CameraRepository
from infrastructure.repositories.camera_parking_place import CameraParkingPlaceRepository
from infrastructure.repositories.place_status import PlaceStatusRepository
from infrastructure.repositories.user import UserRepository
from infrastructure.repositories.violation import ViolationRepository
from infrastructure.repositories.zone_type import ZoneTypeRepository
from infrastructure.repositories.unified_auth import UnifiedAuthRepository

from domain.i_parking_place import IParkingPlace
from domain.i_parking_zone import IParkingZone
from domain.i_admin import IAdmin
from domain.i_booking import IBooking
from domain.i_booking_status import IBookingStatus
from domain.i_car import ICar
from domain.i_car_user import ICarUser
from domain.i_camera import ICamera
from domain.i_camera_parking_place import ICameraParkingPlace
from domain.i_place_status import IPlaceStatus
from domain.i_user import IUser
from domain.i_violation import IViolation
from domain.i_zone_type import IZoneType
from domain.i_unified_auth import IUnifiedAuth

from application.services.interfaces.i_parking_place_service import IParkingPlaceService
from application.services.interfaces.i_parking_zone_service import IParkingZoneService
from application.services.interfaces.i_admin_service import IAdminService
from application.services.interfaces.i_booking_service import IBookingService
from application.services.interfaces.i_booking_status_service import IBookingStatusService
from application.services.interfaces.i_car_service import ICarService
from application.services.interfaces.i_car_user_service import ICarUserService
from application.services.interfaces.i_camera_service import ICameraService
from application.services.interfaces.i_camera_parking_place_service import ICameraParkingPlaceService
from application.services.interfaces.i_place_status_service import IPlaceStatusService
from application.services.interfaces.i_user_service import IUserService
from application.services.interfaces.i_violation_service import IViolationService
from application.services.interfaces.i_zone_type_service import IZoneTypeService
from application.services.interfaces.i_unified_auth_service import IUnifiedAuthService

from application.services.impl.zone_service import ParkingZoneService
from application.services.impl.place_service import ParkingPlaceService
from application.services.impl.admin_service import AdminService
from application.services.impl.booking_service import BookingService
from application.services.impl.booking_status_service import BookingStatusService
from application.services.impl.car_service import CarService
from application.services.impl.car_user_service import CarUserService
from application.services.impl.camera_service import CameraService
from application.services.impl.camera_parking_place_service import CameraParkingPlaceService
from application.services.impl.place_status_service import PlaceStatusService
from application.services.impl.user_service import UserService
from application.services.impl.violation_service import ViolationService
from application.services.impl.zone_type_service import ZoneTypeService
from application.services.impl.unified_auth_service import UnifiedAuthService

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

    _register_services(container)

    return container


def _register_repositories(container: punq.Container) -> None:
    db = container.resolve(Database)
    
    container.register(IParkingZone, factory=lambda: ParkingZoneRepository(db))
    container.register(IParkingPlace, factory=lambda: ParkingPlaceRepository(db))
    container.register(IAdmin, factory=lambda: AdminRepository(db))
    container.register(IBooking, factory=lambda: BookingRepository(db))
    container.register(IBookingStatus, factory=lambda: BookingStatusRepository(db))
    container.register(ICar, factory=lambda: CarRepository(db))
    container.register(ICarUser, factory=lambda: CarUserRepository(db))
    container.register(ICamera, factory=lambda: CameraRepository(db))
    container.register(ICameraParkingPlace, factory=lambda: CameraParkingPlaceRepository(db))
    container.register(IPlaceStatus, factory=lambda: PlaceStatusRepository(db))
    container.register(IUser, factory=lambda: UserRepository(db))
    container.register(IViolation, factory=lambda: ViolationRepository(db))
    container.register(IZoneType, factory=lambda: ZoneTypeRepository(db))
    container.register(IUnifiedAuth, factory=lambda: UnifiedAuthRepository(db))


def _register_services(container: punq.Container) -> None:
    container.register(IParkingZoneService, factory=lambda: ParkingZoneService(container.resolve(IParkingZone)))
    container.register(IParkingPlaceService, factory=lambda: ParkingPlaceService(container.resolve(IParkingPlace)))
    container.register(IAdminService, factory=lambda: AdminService(container.resolve(IAdmin)))
    container.register(IBookingService, factory=lambda: BookingService(container.resolve(IBooking)))
    container.register(IBookingStatusService, factory=lambda: BookingStatusService(container.resolve(IBookingStatus)))
    container.register(ICarService, factory=lambda: CarService(container.resolve(ICar)))
    container.register(ICarUserService, factory=lambda: CarUserService(container.resolve(ICarUser)))
    container.register(ICameraService, factory=lambda: CameraService(container.resolve(ICamera)))
    container.register(ICameraParkingPlaceService, factory=lambda: CameraParkingPlaceService(container.resolve(ICameraParkingPlace)))
    container.register(IPlaceStatusService, factory=lambda: PlaceStatusService(container.resolve(IPlaceStatus)))
    container.register(IUserService, factory=lambda: UserService(container.resolve(IUser)))
    container.register(IViolationService, factory=lambda: ViolationService(container.resolve(IViolation)))
    container.register(IZoneTypeService, factory=lambda: ZoneTypeService(container.resolve(IZoneType)))
    
    container.register(IUnifiedAuthService, factory=lambda: UnifiedAuthService(
        container.resolve(IUnifiedAuth), 
        container.resolve(IUser), 
        container.resolve(IAdmin)
    ))
