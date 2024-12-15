from models import ParkingZone, ParkingPlace
from schemas import (
    ParkingZoneCreate,
    ParkingZoneResponse,
    ParkingPlaceCreate,
    ParkingPlaceResponse
)

class ParkingZoneMapper:
    @staticmethod
    def to_entity(dto: ParkingZoneCreate) -> ParkingZone:
        """
        Преобразует ParkingZoneCreate в ParkingZone (Entity)
        """
        return ParkingZone(
            name=dto.name,
            coordinates=dto.coordinates
        )

    @staticmethod
    def to_response(entity: ParkingZone) -> ParkingZoneResponse:
        """
        Преобразует ParkingZone (Entity) в ParkingZoneResponse (DTO)
        """
        return ParkingZoneResponse(
            id=entity.id,
            name=entity.name,
            coordinates=entity.coordinates
        )


class ParkingPlaceMapper:
    @staticmethod
    def to_entity(dto: ParkingPlaceCreate) -> ParkingPlace:
        """
        Преобразует ParkingPlaceCreate в ParkingPlace (Entity)
        """
        return ParkingPlace(
            number=dto.number,
            zone_id=dto.zone_id
        )

    @staticmethod
    def to_response(entity: ParkingPlace) -> ParkingPlaceResponse:
        """
        Преобразует ParkingPlace (Entity) в ParkingPlaceResponse (DTO)
        """
        return ParkingPlaceResponse(
            id=entity.id,
            number=entity.number,
            zone_id=entity.zone_id
        )
