from repositories.impl.parking_zone import ParkingZoneRepository
from models import ParkingZone
from schemas import ParkingZoneCreate
from fastapi import HTTPException
from mapper import ParkingZoneMapper

class ZoneService:
    def __init__(self, zone_repo: ParkingZoneRepository):
        self.zone_repo = zone_repo

    async def create_zone(self, zone_data: ParkingZoneCreate):
        if zone_data.coordinates[0] != zone_data.coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed")

        zone = ParkingZoneMapper.to_entity(zone_data)
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

    async def update_zone(self, zone_id: int, zone_data: ParkingZoneCreate):
        # Проверка, существует ли зона
        zone = await self.zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise HTTPException(status_code=404, detail="Zone not found")

        if zone_data.coordinates[0] != zone_data.coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed")

        zone.name = zone_data.name
        zone.coordinates = zone_data.coordinates

        return await self.zone_repo.save(zone)