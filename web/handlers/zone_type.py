from fastapi import APIRouter, Depends, HTTPException
from typing import List

from web.container import get_container
from web.schemas import ZoneTypeCreate, ZoneTypeResponse
from application.services.interfaces.i_zone_type_service import IZoneTypeService

router = APIRouter(prefix="/zone-type", tags=["zone-type"])

def get_zone_type_service() -> IZoneTypeService:
    return get_container().resolve(IZoneTypeService)

@router.post("/", response_model=ZoneTypeResponse)
async def create_zone_type(data: ZoneTypeCreate, service: IZoneTypeService = Depends(get_zone_type_service)):
    try:
        return await service.create_zone_type(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{type_id}", response_model=ZoneTypeResponse)
async def get_zone_type(type_id: int, service: IZoneTypeService = Depends(get_zone_type_service)):
    try:
        return await service.get_zone_type(type_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[ZoneTypeResponse])
async def get_all_zone_types(service: IZoneTypeService = Depends(get_zone_type_service)):
    return await service.list_all_types()

@router.put("/{type_id}", response_model=ZoneTypeResponse)
async def update_zone_type(type_id: int, data: ZoneTypeCreate, service: IZoneTypeService = Depends(get_zone_type_service)):
    try:
        return await service.update_zone_type(type_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{type_id}")
async def delete_zone_type(type_id: int, service: IZoneTypeService = Depends(get_zone_type_service)):
    try:
        await service.delete_zone_type(type_id)
        return {"message": "Zone type deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 