from typing import List, Union
from web.schemas import ParkingZoneCreate, ParkingZoneResponse, ParkingZoneDetailedResponse
from application.services.interfaces.i_parking_zone_service import IParkingZoneService
from infrastructure.repositories.parking_zone import ParkingZoneRepository
from fastapi import HTTPException
from web.mapper import ParkingZoneMapper
from domain.models import ParkingZone

class ParkingZoneService(IParkingZoneService):
    def __init__(self, parking_zone_repo: ParkingZoneRepository):
        self.parking_zone_repo = parking_zone_repo
        self.mapper = ParkingZoneMapper()

    def _validate_polygon(self, coordinates: List[List[float]]) -> None:
        if not coordinates or len(coordinates) < 3:
            raise HTTPException(status_code=400, detail="Polygon must have at least 3 points")
        if coordinates[0] != coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed (first and last points must be the same)")

    async def create_zone(self, data: ParkingZoneCreate) -> ParkingZoneResponse:
        self._validate_polygon(data.location)
        zone = self.mapper.to_entity(data)
        created_zone = await self.parking_zone_repo.save(zone)
        return self.mapper.to_response(created_zone)

    async def get_zone(self, zone_id: int) -> ParkingZoneResponse:
        zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise ValueError(f"Parking zone with id {zone_id} not found")
        return self.mapper.to_response(zone)

    async def get_all_zones(self) -> List[ParkingZoneResponse]:
        zones = await self.parking_zone_repo.get_by_all(ParkingZone)
        return [self.mapper.to_response(zone) for zone in zones]

    async def update_zone(self, zone_id: int, data: ParkingZoneCreate) -> ParkingZoneResponse:
        self._validate_polygon(data.location)
        zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise ValueError(f"Parking zone with id {zone_id} not found")
        
        updated_zone = self.mapper.to_entity(data)
        updated_zone.id = zone_id
        
        updated_zone = await self.parking_zone_repo.update(updated_zone)
        return self.mapper.to_response(updated_zone)

    async def delete_zone(self, zone_id: Union[int, str]) -> None:
        zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise ValueError(f"Parking zone with id {zone_id} not found")
        await self.parking_zone_repo.delete(zone)

    async def get_zones_by_admin(self, admin_id: int) -> List[ParkingZoneResponse]:
        zones = await self.parking_zone_repo.list_by_admin(admin_id)
        return [self.mapper.to_response(zone) for zone in zones]

    async def get_zone_detailed(self, zone_id: int) -> ParkingZoneDetailedResponse:
        result = await self.parking_zone_repo.get_zone_detailed(zone_id)
        if not result:
            raise ValueError(f"Parking zone with id {zone_id} not found")
            
        zone, zone_type, total_places, free_places, occupied_places, total_cameras = result
        
        return ParkingZoneDetailedResponse(
            id=zone.id,
            zone_name=zone.zone_name,
            type_name=zone_type.type_name,
            address=zone.address,
            start_time=zone.start_time,
            end_time=zone.end_time,
            price_per_minute=zone.price_per_minute,
            location=zone.location,
            total_places=total_places,
            free_places=free_places,
            occupied_places=occupied_places,
            total_cameras=total_cameras
        )