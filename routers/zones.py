from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas import ParkingZoneCreate, ParkingZoneResponse
from services.parking_service import ParkingService
from repositories.parking_zone import ParkingZoneRepository

router = APIRouter(prefix="/zones", tags=["zones"])


@router.post("/", response_model=ParkingZoneResponse)
async def create_zone(zone: ParkingZoneCreate, db: AsyncSession = Depends(get_db)):
    service = ParkingService(ParkingZoneRepository(db), None)
    return await service.create_zone(zone)


@router.get("/", response_model=List[ParkingZoneResponse])
async def get_all_zones(db: AsyncSession = Depends(get_db)):
    service = ParkingService(ParkingZoneRepository(db), None)
    return await service.get_all_zones()


@router.get("/{zone_id}", response_model=ParkingZoneResponse)
async def get_zone(zone_id: int, db: AsyncSession = Depends(get_db)):
    service = ParkingService(ParkingZoneRepository(db), None)
    return await service.get_zone(zone_id)
