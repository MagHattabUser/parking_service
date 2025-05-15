from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import CarUserCreate, CarUserResponse
from application.services.interfaces.i_car_user_service import ICarUserService

router = APIRouter(prefix="/car-user", tags=["car-user"])

def get_car_user_service() -> ICarUserService:
    return get_container().resolve(ICarUserService)

@router.post("/", response_model=CarUserResponse)
async def create_car_user(data: CarUserCreate, service: ICarUserService = Depends(get_car_user_service)):
    return await service.create_car_user(data)

@router.get("/{id}", response_model=CarUserResponse)
async def get_car_user(id: int, service: ICarUserService = Depends(get_car_user_service)):
    return await service.get_car_user(id)

@router.get("/", response_model=List[CarUserResponse])
async def get_all_car_users(service: ICarUserService = Depends(get_car_user_service)):
    return await service.get_all_car_users()

@router.put("/{id}", response_model=CarUserResponse)
async def update_car_user(id: int, data: CarUserCreate, service: ICarUserService = Depends(get_car_user_service)):
    return await service.update_car_user(id, data)

@router.delete("/{id}")
async def delete_car_user(id: int, service: ICarUserService = Depends(get_car_user_service)):
    await service.delete_car_user(id)
    return {"message": "Car-User connection deleted successfully"}

@router.post("/assign", response_model=CarUserResponse, summary="Привязка автомобиля к пользователю")
async def assign_car(data: CarUserCreate, service: ICarUserService = Depends(get_car_user_service)):
    return await service.assign_car(data)

@router.delete("/unassign/{car_user_id}", summary="Отвязка автомобиля от пользователя")
async def unassign_car(car_user_id: int, service: ICarUserService = Depends(get_car_user_service)):
    await service.unassign_car(car_user_id)
    return {"message": "Car unassigned from user successfully"}

@router.get("/user/{user_id}", response_model=List[CarUserResponse], summary="Машины пользователя")
async def list_by_user(user_id: int, service: ICarUserService = Depends(get_car_user_service)):
    return await service.list_by_user(user_id)

@router.get("/car/{car_id}", response_model=List[CarUserResponse], summary="Пользователи машины")
async def list_by_car(car_id: int, service: ICarUserService = Depends(get_car_user_service)):
    return await service.list_by_car(car_id)