from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import CameraParkingPlaceCreate, CameraParkingPlaceResponse
from application.services.interfaces.i_camera_parking_place_service import ICameraParkingPlaceService

router = APIRouter(prefix="/camera-parking-place", tags=["camera-parking-place"])

def get_camera_parking_place_service() -> ICameraParkingPlaceService:
    return get_container().resolve(ICameraParkingPlaceService)

@router.post("/", response_model=CameraParkingPlaceResponse)
async def create_camera_parking_place(data: CameraParkingPlaceCreate, service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    return await service.create_camera_parking_place(data)

@router.get("/{id}", response_model=CameraParkingPlaceResponse)
async def get_camera_parking_place(id: int, service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    return await service.get_camera_parking_place(id)

@router.get("/", response_model=List[CameraParkingPlaceResponse])
async def get_all_camera_parking_places(service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    return await service.get_all_camera_parking_places()

@router.put("/{id}", response_model=CameraParkingPlaceResponse)
async def update_camera_parking_place(id: int, data: CameraParkingPlaceCreate, service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    return await service.update_camera_parking_place(id, data)

@router.delete("/{id}")
async def delete_camera_parking_place(id: int, service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    await service.delete_camera_parking_place(id)
    return {"message": "Camera-ParkingPlace connection deleted successfully"}

@router.get("/camera/{camera_id}", response_model=List[CameraParkingPlaceResponse])
async def list_places_for_camera(camera_id: int, service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    """
    Получить все парковочные места, связанные с определенной камерой.
    """
    return await service.list_places_for_camera(camera_id)

@router.get("/place/{place_id}", response_model=List[CameraParkingPlaceResponse])
async def list_cameras_for_place(place_id: int, service: ICameraParkingPlaceService = Depends(get_camera_parking_place_service)):
    """
    Получить все камеры, связанные с определенным парковочным местом.
    """
    return await service.list_cameras_for_place(place_id)