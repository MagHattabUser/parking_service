from fastapi import APIRouter, Depends, Response, HTTPException
from typing import List, Dict
import base64
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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
    return await service.list_by_zone(zone_id)

class CameraSnapshot(BaseModel):
    camera_id: int
    image_base64: str
    content_type: str = "image/jpeg"

class ZoneSnapshotsResponse(BaseModel):
    zone_id: int
    snapshots: List[CameraSnapshot]

@router.get("/snapshot/{zone_id}", response_model=ZoneSnapshotsResponse, summary="Получить снимки со всех камер зоны")
async def get_zone_snapshots(zone_id: int, service: ICameraService = Depends(get_camera_service)):
    try:
        snapshots = await service.get_zone_snapshots(zone_id)
        
        camera_snapshots = []
        for camera_id, image_data in snapshots.items():
            base64_image = base64.b64encode(image_data).decode('utf-8')
            camera_snapshots.append(CameraSnapshot(
                camera_id=camera_id,
                image_base64=base64_image
            ))
        
        return ZoneSnapshotsResponse(
            zone_id=zone_id,
            snapshots=camera_snapshots
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении снимков: {str(e)}")