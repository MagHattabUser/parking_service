from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas import ParkingZoneCreate, ParkingZoneResponse
from services.parking_service import ParkingService
from repositories.parking_zone import ParkingZoneRepository
from services.zone_service import ZoneService
from container import get_container

router = APIRouter(prefix="/zones", tags=["zones"])


def get_zone_service() -> ZoneService:
    container = get_container()
    return container.resolve(ZoneService)

@router.post("/", response_model=ParkingZoneResponse)
async def create_zone(zone: ParkingZoneCreate, service: ZoneService = Depends(get_zone_service)):
    return await service.create_zone(zone)


@router.get("/", response_model=List[ParkingZoneResponse])
async def get_all_zones(service: ZoneService = Depends(get_zone_service)):
    return await service.get_all_zones()


@router.get("/{zone_id}", response_model=ParkingZoneResponse)
async def get_zone(zone_id: int, service: ZoneService = Depends(get_zone_service)):
    return await service.get_zone(zone_id)


@router.delete("/zone/{identifier}", response_model=ParkingZoneResponse)
async def delete_zone(identifier: str, service: ZoneService = Depends(get_zone_service)):
    if identifier.isdigit():
        identifier = int(identifier)

    return await service.delete_zone(identifier)
