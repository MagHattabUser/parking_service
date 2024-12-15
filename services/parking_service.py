from repositories.impl.parking_zone import ParkingZoneRepository
from repositories.impl.parking_place import ParkingPlaceRepository
from models import ParkingZone, ParkingPlace
from schemas import ParkingZoneCreate, ParkingPlaceCreate
from fastapi import HTTPException

class ParkingService:
    def __init__(self, zone_repo: ParkingZoneRepository, place_repo: ParkingPlaceRepository):
        self.zone_repo = zone_repo
        self.place_repo = place_repo

    async def get_places_by_zone(self, zona_identifier: str | int):
        return await self.place_repo.get_by_zone(zona_identifier)

    async def create_zone(self, zone_data: ParkingZoneCreate):
        if zone_data.coordinates[0] != zone_data.coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed")

        zone = ParkingZone(**zone_data.dict())
        return await self.zone_repo.save(zone)
    #mapper для преобразование из dto в entity и обратно
    async def create_place(self, place_data: ParkingPlaceCreate):
        place = ParkingPlace(**place_data.dict())
        return await self.place_repo.save(place)

    async def get_all_zones(self):
        return await self.zone_repo.get_all()

    async def get_zone(self, zone_id: int):
        return await self.zone_repo.get_by_id(ParkingZone, zone_id)

    async def delete_zone(self, identifier: str | int):
        zone = await self.zone_repo.delete_by_id_or_name(identifier)
        if not zone:
            raise HTTPException(status_code=404, detail="Zone not found")
        return zone

    async def delete_place(self, place_id: int):
        place = await self.place_repo.delete_by_id(place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        return place
