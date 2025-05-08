from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import CarCreate, CarResponse
from application.services.interfaces.i_car_service import ICarService

router = APIRouter(prefix="/car", tags=["car"])

def get_car_service() -> ICarService:
    return get_container().resolve(ICarService)

@router.post("/", response_model=CarResponse)
async def create_car(data: CarCreate, service: ICarService = Depends(get_car_service)):
    return await service.create_car(data)

@router.get("/{car_id}", response_model=CarResponse)
async def get_car(car_id: int, service: ICarService = Depends(get_car_service)):
    return await service.get_car(car_id)

@router.get("/", response_model=List[CarResponse])
async def get_all_cars(service: ICarService = Depends(get_car_service)):
    return await service.get_all_cars()

@router.put("/{car_id}", response_model=CarResponse)
async def update_car(car_id: int, data: CarCreate, service: ICarService = Depends(get_car_service)):
    return await service.update_car(car_id, data)

@router.delete("/{car_id}")
async def delete_car(car_id: int, service: ICarService = Depends(get_car_service)):
    await service.delete_car(car_id)
    return {"message": "Car deleted successfully"} 