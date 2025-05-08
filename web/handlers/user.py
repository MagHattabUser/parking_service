from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import UserCreate, UserResponse
from application.services.interfaces.i_user_service import IUserService

router = APIRouter(prefix="/user", tags=["user"])

def get_user_service() -> IUserService:
    return get_container().resolve(IUserService)

@router.post("/", response_model=UserResponse)
async def create_user(data: UserCreate, service: IUserService = Depends(get_user_service)):
    return await service.create_user(data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: IUserService = Depends(get_user_service)):
    return await service.get_user(user_id)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(service: IUserService = Depends(get_user_service)):
    return await service.get_all_users()

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserCreate, service: IUserService = Depends(get_user_service)):
    return await service.update_user(user_id, data)

@router.delete("/{user_id}")
async def delete_user(user_id: int, service: IUserService = Depends(get_user_service)):
    await service.delete_user(user_id)
    return {"message": "User deleted successfully"} 