from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import PlaceStatusCreate, PlaceStatusResponse
from application.services.interfaces.i_place_status_service import IPlaceStatusService

router = APIRouter(prefix="/place-status", tags=["place-status"])

def get_place_status_service() -> IPlaceStatusService:
    return get_container().resolve(IPlaceStatusService)

@router.post("/", response_model=PlaceStatusResponse)
async def create_place_status(data: PlaceStatusCreate, service: IPlaceStatusService = Depends(get_place_status_service)):
    return await service.create_place_status(data)

@router.get("/{status_id}", response_model=PlaceStatusResponse)
async def get_place_status(status_id: int, service: IPlaceStatusService = Depends(get_place_status_service)):
    return await service.get_place_status(status_id)

@router.get("/", response_model=List[PlaceStatusResponse])
async def get_all_place_statuses(service: IPlaceStatusService = Depends(get_place_status_service)):
    return await service.list_all_statuses()

@router.put("/{status_id}", response_model=PlaceStatusResponse)
async def update_place_status(status_id: int, data: PlaceStatusCreate, service: IPlaceStatusService = Depends(get_place_status_service)):
    return await service.update_place_status(status_id, data)

@router.delete("/{status_id}")
async def delete_place_status(status_id: int, service: IPlaceStatusService = Depends(get_place_status_service)):
    await service.delete_place_status(status_id)
    return {"message": "Place status deleted successfully"} 