from repositories.parking_zone import ParkingZoneRepository
from repositories.parking_place import ParkingPlaceRepository
from models import ParkingZone, ParkingPlace
from schemas import ParkingZoneCreate, ParkingPlaceCreate
from fastapi import HTTPException

class ZoneService:
    def __init__(self, zone_repo: ParkingZoneRepository):
        self.zone_repo = zone_repo

    async def create_zone(self, zone_data: ParkingZoneCreate):
        if zone_data.coordinates[0] != zone_data.coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed")

        zone = ParkingZone(**zone_data.dict())
        return await self.zone_repo.save(zone)

    async def get_all_zones(self):
        return await self.zone_repo.get_all()

    async def get_zone(self, zone_id: int):
        return await self.zone_repo.get_by_id(ParkingZone, zone_id)

    async def delete_zone(self, identifier: str | int):
        zone = await self.zone_repo.delete_by_id_or_name(identifier)
        if not zone:
            raise HTTPException(status_code=404, detail="Zone not found")
        return zone