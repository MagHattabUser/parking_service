from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated

from domain.models import User
from web.handlers.unified_auth import get_current_user, get_current_admin

from web.schemas import ZoneTypeCreate, ZoneTypeResponse
from application.services.interfaces.i_zone_type_service import IZoneTypeService
from web.container import get_container

router = APIRouter(prefix="/zone-types", tags=["zone-types"])


def get_zone_type_service() -> IZoneTypeService:
    return get_container().resolve(IZoneTypeService)


@router.post("/", response_model=ZoneTypeResponse)
async def create_zone_type(
    data: ZoneTypeCreate, 
    #current_user: Annotated[User, Depends(get_current_user)],
    service: IZoneTypeService = Depends(get_zone_type_service)
):
    try:
        return await service.create_zone_type(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ZoneTypeResponse])
async def list_all_types(
    #current_user: Annotated[User, Depends(get_current_user)],
    service: IZoneTypeService = Depends(get_zone_type_service)
):
    return await service.list_all_types()


@router.get("/{zone_type_id}", response_model=ZoneTypeResponse)
async def get_zone_type(
    zone_type_id: int, 
    #current_user: Annotated[User, Depends(get_current_user)],
    service: IZoneTypeService = Depends(get_zone_type_service)
):
    try:
        return await service.get_zone_type(zone_type_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{zone_type_id}", response_model=ZoneTypeResponse)
async def update_zone_type(
    zone_type_id: int, 
    data: ZoneTypeCreate, 
    #current_user: Annotated[User, Depends(get_current_user)],
    service: IZoneTypeService = Depends(get_zone_type_service)
):
    try:
        return await service.update_zone_type(zone_type_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{zone_type_id}")
async def delete_zone_type(
    zone_type_id: int, 
    #current_admin: Annotated[User, Depends(get_current_admin)],
    service: IZoneTypeService = Depends(get_zone_type_service)
):
    try:
        await service.delete_zone_type(zone_type_id)
        return {"message": "Zone type deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
