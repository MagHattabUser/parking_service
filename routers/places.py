from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas import ParkingPlaceCreate, ParkingPlaceResponse
from services.parking_service import ParkingService
from repositories.parking_place import ParkingPlaceRepository

router = APIRouter(prefix="/places", tags=["places"])


#create_session global
# DI контейнер
@router.post("/", response_model=ParkingPlaceResponse)
async def create_place(place: ParkingPlaceCreate, db: AsyncSession = Depends(get_db)):
    service = ParkingService(None, ParkingPlaceRepository(db))
    return await service.create_place(place)


@router.get("/zone/{zone_identifier}", response_model=List[ParkingPlaceResponse])
async def get_places_by_zone(zone_identifier: str, db: AsyncSession = Depends(get_db)):
    service = ParkingService(None, ParkingPlaceRepository(db))

    if zone_identifier.isdigit():
        zone_identifier = int(zone_identifier)

    return await service.get_places_by_zone(zone_identifier)

@router.delete("/place/{place_id}", response_model=ParkingPlaceResponse)
async def delete_place(place_id: int, db: AsyncSession = Depends(get_db)):
    service = ParkingService(None, ParkingPlaceRepository(db))
    return await service.delete_place(place_id)