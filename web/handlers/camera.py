from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import CameraCreate, CameraResponse
from application.services.interfaces.i_camera_service import ICameraService

router = APIRouter(prefix="/camera", tags=["camera"])

def get_camera_service() -> ICameraService:
    return get_container().resolve(ICameraService)

@router.post("/", response_model=CameraResponse)
async def create_camera(data: CameraCreate, service: ICameraService = Depends(get_camera_service)):
    return await service.create_camera(data)

@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: int, service: ICameraService = Depends(get_camera_service)):
    return await service.get_camera(camera_id)

@router.get("/", response_model=List[CameraResponse])
async def get_all_cameras(service: ICameraService = Depends(get_camera_service)):
    return await service.get_all_cameras()

@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(camera_id: int, data: CameraCreate, service: ICameraService = Depends(get_camera_service)):
    return await service.update_camera(camera_id, data)

@router.delete("/{camera_id}")
async def delete_camera(camera_id: int, service: ICameraService = Depends(get_camera_service)):
    await service.delete_camera(camera_id)
    return {"message": "Camera deleted successfully"}

@router.get("/zone/{zone_id}", response_model=List[CameraResponse], summary="Камеры парковочной зоны")
async def get_cameras_by_zone(zone_id: int, service: ICameraService = Depends(get_camera_service)):
    """Возвращает все камеры, установленные в конкретной парковочной зоне"""
    return await service.list_by_zone(zone_id)