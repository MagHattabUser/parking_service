from repositories.parking_zone import ParkingZoneRepository
from repositories.parking_place import ParkingPlaceRepository
from models import ParkingZone, ParkingPlace
from schemas import ParkingZoneCreate, ParkingPlaceCreate
from fastapi import HTTPException

class ParkingService:
    def __init__(self, zone_repo: ParkingZoneRepository, place_repo: ParkingPlaceRepository):
        self.zone_repo = zone_repo
        self.place_repo = place_repo

    async def get_places_by_zona(self, zona_identifier: str | int):
        return await self.place_repo.get_by_zone(zona_identifier)

    async def create_zone(self, zone_data: ParkingZoneCreate):
        if zone_data.coordinates[0] != zone_data.coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed")

        zone = ParkingZone(**zone_data.dict())
        return await self.zone_repo.save(zone)

    async def create_place(self, place_data: ParkingPlaceCreate):
        place = ParkingPlace(**place_data.dict())
        return await self.place_repo.save(place)
