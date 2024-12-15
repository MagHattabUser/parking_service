from fastapi import APIRouter, Depends
from typing import List

from schemas import ParkingPlaceCreate, ParkingPlaceResponse
from services.place_service import PlaceService
from container import get_container

router = APIRouter(prefix="/places", tags=["places"])

def get_place_service() -> PlaceService:
    container = get_container()
    return container.resolve(PlaceService)

@router.post("/", response_model=ParkingPlaceResponse)
async def create_place(place: ParkingPlaceCreate, service: PlaceService = Depends(get_place_service)):
    return await service.create_place(place)


@router.get("/zone/{zone_identifier}", response_model=List[ParkingPlaceResponse])
async def get_places_by_zone(zone_identifier: str, service: PlaceService = Depends(get_place_service)):
    if zone_identifier.isdigit():
        zone_identifier = int(zone_identifier)

    return await service.get_places_by_zone(zone_identifier)


@router.delete("/place/{place_id}", response_model=ParkingPlaceResponse)
async def delete_place(place_id: int, service: PlaceService = Depends(get_place_service)):
    return await service.delete_place(place_id)