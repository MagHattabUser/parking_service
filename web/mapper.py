from domain.models import (
    User, Car, CarUser, Booking, BookingStatus,
    PlaceStatus, ZoneType, Admin, ParkingZone,
    Camera, CameraParkingPlace, ParkingPlace, Violation
)
from web.schemas import (
    UserCreate, UserResponse,
    CarCreate, CarResponse,
    CarUserCreate, CarUserResponse,
    BookingCreate, BookingResponse,
    BookingStatusCreate, BookingStatusResponse,
    PlaceStatusCreate, PlaceStatusResponse,
    ZoneTypeCreate, ZoneTypeResponse,
    AdminCreate, AdminResponse,
    ParkingZoneCreate, ParkingZoneResponse,
    CameraCreate, CameraResponse,
    CameraParkingPlaceCreate, CameraParkingPlaceResponse,
    ParkingPlaceCreate, ParkingPlaceResponse,
    ViolationCreate, ViolationResponse
)


class UserMapper:
    @staticmethod
    def to_entity(dto: UserCreate) -> User:
        return User(
            user_name=dto.user_name,
            phone=dto.phone,
            password=dto.password,
            email=dto.email
        )

    @staticmethod
    def to_response(entity: User) -> UserResponse:
        return UserResponse(
            id=entity.id,
            user_name=entity.user_name,
            phone=entity.phone,
            email=entity.email
        )


class CarMapper:
    @staticmethod
    def to_entity(dto: CarCreate) -> Car:
        return Car(car_number=dto.car_number)

    @staticmethod
    def to_response(entity: Car) -> CarResponse:
        return CarResponse(id=entity.id, car_number=entity.car_number)


class CarUserMapper:
    @staticmethod
    def to_entity(dto: CarUserCreate) -> CarUser:
        return CarUser(user_id=dto.user_id, car_id=dto.car_id)

    @staticmethod
    def to_response(entity: CarUser) -> CarUserResponse:
        return CarUserResponse(
            id=entity.id,
            user_id=entity.user_id,
            car_id=entity.car_id
        )


class BookingMapper:
    @staticmethod
    def to_entity(dto: BookingCreate) -> Booking:
        return Booking(
            car_user_id=dto.car_user_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            parking_place_id=dto.parking_place_id,
            booking_status_id=dto.booking_status_id
        )

    @staticmethod
    def to_response(entity: Booking) -> BookingResponse:
        return BookingResponse(
            id=entity.id,
            car_user_id=entity.car_user_id,
            start_time=entity.start_time,
            end_time=entity.end_time,
            parking_place_id=entity.parking_place_id,
            booking_status_id=entity.booking_status_id
        )


class BookingStatusMapper:
    @staticmethod
    def to_entity(dto: BookingStatusCreate) -> BookingStatus:
        return BookingStatus(
            status_name=dto.status_name
        )

    @staticmethod
    def to_response(entity: BookingStatus) -> BookingStatusResponse:
        return BookingStatusResponse(id=entity.id, status_name=entity.status_name)


class PlaceStatusMapper:
    @staticmethod
    def to_entity(dto: PlaceStatusCreate) -> PlaceStatus:
        return PlaceStatus(
            status_name=dto.status_name
        )

    @staticmethod
    def to_response(entity: PlaceStatus) -> PlaceStatusResponse:
        return PlaceStatusResponse(id=entity.id, status_name=entity.status_name)


class ZoneTypeMapper:
    @staticmethod
    def to_entity(dto: ZoneTypeCreate) -> ZoneType:
        return ZoneType(
            type_name=dto.type_name
        )

    @staticmethod
    def to_response(entity: ZoneType) -> ZoneTypeResponse:
        return ZoneTypeResponse(id=entity.id, type_name=entity.type_name)


class AdminMapper:
    @staticmethod
    def to_entity(dto: AdminCreate) -> Admin:
        return Admin(
            admin_name=dto.admin_name,
            email=dto.email,
            password=dto.password
        )

    @staticmethod
    def to_response(entity: Admin) -> AdminResponse:
        return AdminResponse(
            id=entity.id,
            admin_name=entity.admin_name,
            email=entity.email
        )


class ParkingZoneMapper:
    @staticmethod
    def to_entity(dto: ParkingZoneCreate) -> ParkingZone:
        return ParkingZone(
            zone_name=dto.zone_name,
            zone_type_id=dto.zone_type_id,
            address=dto.address,
            start_time=dto.start_time,
            end_time=dto.end_time,
            price_per_minute=dto.price_per_minute,
            location=dto.location,
            update_time=dto.update_time,
            admin_id=dto.admin_id
        )

    @staticmethod
    def to_response(entity: ParkingZone) -> ParkingZoneResponse:
        return ParkingZoneResponse(
            id=entity.id,
            zone_name=entity.zone_name,
            zone_type_id=entity.zone_type_id,
            address=entity.address,
            start_time=entity.start_time,
            end_time=entity.end_time,
            price_per_minute=entity.price_per_minute,
            location=entity.location,
            update_time=entity.update_time,
            admin_id=entity.admin_id
        )


class CameraMapper:
    @staticmethod
    def to_entity(dto: CameraCreate) -> Camera:
        return Camera(
            camera_name=dto.camera_name,
            url=dto.url,
            parking_zone_id=dto.parking_zone_id
        )

    @staticmethod
    def to_response(entity: Camera) -> CameraResponse:
        return CameraResponse(
            id=entity.id,
            camera_name=entity.camera_name,
            url=entity.url,
            parking_zone_id=entity.parking_zone_id
        )


class CameraParkingPlaceMapper:
    @staticmethod
    def to_entity(dto: CameraParkingPlaceCreate) -> CameraParkingPlace:
        return CameraParkingPlace(
            camera_id=dto.camera_id,
            parking_place_id=dto.parking_place_id,
            location=dto.location
        )

    @staticmethod
    def to_response(entity: CameraParkingPlace) -> CameraParkingPlaceResponse:
        return CameraParkingPlaceResponse(
            id=entity.id,
            camera_id=entity.camera_id,
            parking_place_id=entity.parking_place_id,
            location=entity.location
        )


class ParkingPlaceMapper:
    @staticmethod
    def to_entity(dto: ParkingPlaceCreate) -> ParkingPlace:
        return ParkingPlace(
            place_number=dto.place_number,
            place_status_id=dto.place_status_id,
            parking_zone_id=dto.parking_zone_id
        )

    @staticmethod
    def to_response(entity: ParkingPlace) -> ParkingPlaceResponse:
        return ParkingPlaceResponse(
            id=entity.id,
            place_number=entity.place_number,
            place_status_id=entity.place_status_id,
            parking_zone_id=entity.parking_zone_id
        )


class ViolationMapper:
    @staticmethod
    def to_entity(dto: ViolationCreate) -> Violation:
        return Violation(
            car_number=dto.car_number,
            timestamp=dto.timestamp,
            parking_place_id=dto.parking_place_id
        )

    @staticmethod
    def to_response(entity: Violation) -> ViolationResponse:
        return ViolationResponse(
            id=entity.id,
            car_number=entity.car_number,
            timestamp=entity.timestamp,
            parking_place_id=entity.parking_place_id
        )
