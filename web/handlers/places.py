from fastapi import APIRouter, Depends, HTTPException
from typing import List

from web.schemas import ParkingPlaceCreate, ParkingPlaceResponse
from application.services.interfaces.i_parking_place_service import IParkingPlaceService
from web.container import get_container

router = APIRouter(prefix="/places", tags=["places"])

def get_place_service() -> IParkingPlaceService:
    return get_container().resolve(IParkingPlaceService)

@router.post("/", response_model=ParkingPlaceResponse)
async def create_place(data: ParkingPlaceCreate, service: IParkingPlaceService = Depends(get_place_service)):
    try:
        return await service.create_place(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ParkingPlaceResponse])
async def get_all_places(service: IParkingPlaceService = Depends(get_place_service)):
    return await service.get_all_places()

@router.get("/{place_id}", response_model=ParkingPlaceResponse)
async def get_place(place_id: int, service: IParkingPlaceService = Depends(get_place_service)):
    try:
        return await service.get_place(place_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/zone/{zone_id}", response_model=List[ParkingPlaceResponse])
async def get_places_by_zone(zone_id: int, service: IParkingPlaceService = Depends(get_place_service)):
    try:
        return await service.list_by_zone(zone_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/status/{status_id}", response_model=List[ParkingPlaceResponse])
async def get_places_by_status(status_id: int, service: IParkingPlaceService = Depends(get_place_service)):
    try:
        return await service.list_by_status(status_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{place_id}", response_model=ParkingPlaceResponse)
async def update_place(place_id: int, data: ParkingPlaceCreate, service: IParkingPlaceService = Depends(get_place_service)):
    try:
        return await service.update_place(place_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{place_id}")
async def delete_place(place_id: int, service: IParkingPlaceService = Depends(get_place_service)):
    try:
        await service.delete_place(place_id)
        return {"message": "Parking place deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))