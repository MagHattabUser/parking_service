from fastapi import FastAPI, Depends, HTTPException
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.parking_zone import ParkingZoneRepository
from repositories.parking_place import ParkingPlaceRepository
from services.parking_service import ParkingService
from schemas import ParkingZoneCreate, ParkingZoneResponse, ParkingPlaceCreate, ParkingPlaceResponse

app = FastAPI()

@app.post("/zones/", response_model=ParkingZoneResponse)
async def create_zone(
    zone_data: ParkingZoneCreate,
    db: AsyncSession = Depends(get_db),
):
    zone_repo = ParkingZoneRepository(db)
    place_repo = ParkingPlaceRepository(db)
    service = ParkingService(zone_repo, place_repo)

    return await service.create_zone(zone_data)


@app.post("/places/", response_model=ParkingPlaceResponse)
async def create_place(
    place_data: ParkingPlaceCreate,
    db: AsyncSession = Depends(get_db),
):
    zone_repo = ParkingZoneRepository(db)
    place_repo = ParkingPlaceRepository(db)
    service = ParkingService(zone_repo, place_repo)

    return await service.create_place(place_data)
