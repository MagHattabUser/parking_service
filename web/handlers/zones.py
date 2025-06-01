from fastapi import APIRouter, Depends, HTTPException
from typing import List

from web.schemas import (
    ParkingZoneCreate, 
    ParkingZoneResponse, 
    ParkingZoneDetailedResponse,
    PlaceStatusUpdateResponse
)
from application.services.interfaces.i_parking_zone_service import IParkingZoneService
from web.container import get_container

router = APIRouter(prefix="/zones", tags=["zones"])


def get_zone_service() -> IParkingZoneService:
    return get_container().resolve(IParkingZoneService)

@router.post("/", response_model=ParkingZoneResponse)
async def create_zone(data: ParkingZoneCreate, service: IParkingZoneService = Depends(get_zone_service)):
    try:
        return await service.create_zone(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ParkingZoneResponse])
async def get_all_zones(service: IParkingZoneService = Depends(get_zone_service)):
    return await service.get_all_zones()


@router.get("/{zone_id}", response_model=ParkingZoneResponse)
async def get_zone(zone_id: int, service: IParkingZoneService = Depends(get_zone_service)):
    try:
        return await service.get_zone(zone_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{zone_id}", response_model=ParkingZoneResponse)
async def update_zone(zone_id: int, data: ParkingZoneCreate, service: IParkingZoneService = Depends(get_zone_service)):
    try:
        return await service.update_zone(zone_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{zone_id}")
async def delete_zone(zone_id: int, service: IParkingZoneService = Depends(get_zone_service)):
    try:
        await service.delete_zone(zone_id)
        return {"message": "Zone deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/admin/{admin_id}", response_model=List[ParkingZoneResponse], summary="Get Zones By Admin")
async def get_zones_by_admin(admin_id: int, service: IParkingZoneService = Depends(get_zone_service)):
    try:
        return await service.get_zones_by_admin(admin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{zone_id}/detailed", response_model=ParkingZoneDetailedResponse, summary="Get Zone Detailed Information")
async def get_zone_detailed(zone_id: int, service: IParkingZoneService = Depends(get_zone_service)):
    try:
        return await service.get_detailed_info(zone_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{zone_id}/process-image", response_model=PlaceStatusUpdateResponse, summary="Process Zone Image and Update Parking Places Status")
async def process_zone_image(zone_id: int, service: IParkingZoneService = Depends(get_zone_service)):
    """
    Обрабатывает изображение зоны парковки и обновляет статусы мест.
    
    - **zone_id**: ID зоны парковки
    
    Возвращает информацию о количестве обновленных мест.
    """
    try:
        return await service.process_zone_image(zone_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing zone image: {str(e)}")

