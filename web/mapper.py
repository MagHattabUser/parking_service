from domain.models import ParkingZone, ParkingPlace
from web.schemas import (
    ParkingZoneCreate,
    ParkingZoneResponse,
    ParkingPlaceCreate,
    ParkingPlaceResponse
)

class ParkingZoneMapper:
    @staticmethod
    def to_entity(dto: ParkingZoneCreate) -> ParkingZone:
        return ParkingZone(
            name=dto.name,
            coordinates=dto.coordinates
        )

    @staticmethod
    def to_response(entity: ParkingZone) -> ParkingZoneResponse:
        return ParkingZoneResponse(
            id=entity.id,
            name=entity.name,
            coordinates=entity.coordinates
        )


class ParkingPlaceMapper:
    @staticmethod
    def to_entity(dto: ParkingPlaceCreate) -> ParkingPlace:
        return ParkingPlace(
            number=dto.number,
            zone_id=dto.zone_id
        )

    @staticmethod
    def to_response(entity: ParkingPlace) -> ParkingPlaceResponse:
        return ParkingPlaceResponse(
            id=entity.id,
            number=entity.number,
            zone_id=entity.zone_id
        )
