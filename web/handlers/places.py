from fastapi import APIRouter, Depends
from typing import List

from web.schemas import ParkingPlaceCreate, ParkingPlaceResponse
from application.services.i_place_service import IPlaceService
from web.container import get_container

router = APIRouter(prefix="/places", tags=["places"])

def get_place_service() -> IPlaceService:
    container = get_container()
    return container.resolve(IPlaceService)

@router.post("/", response_model=ParkingPlaceResponse)
async def create_place(place: ParkingPlaceCreate, service: IPlaceService = Depends(get_place_service)):
    return await service.create_place(place)


@router.get("/zone/{zone_identifier}", response_model=List[ParkingPlaceResponse])
async def get_places_by_zone(zone_identifier: str, service: IPlaceService = Depends(get_place_service)):
    if zone_identifier.isdigit():
        zone_identifier = int(zone_identifier)

    return await service.get_places_by_zone(zone_identifier)


@router.delete("/place/{place_id}", response_model=ParkingPlaceResponse)
async def delete_place(place_id: int, service: IPlaceService = Depends(get_place_service)):
    return await service.delete_place(place_id)