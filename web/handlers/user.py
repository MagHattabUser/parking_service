from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated

from web.container import get_container
from web.schemas import UserCreate, UserResponse, User
from web.handlers.unified_auth import get_current_user
from application.services.interfaces.i_user_service import IUserService
from domain.models import User as UserModel

router = APIRouter(prefix="/user", tags=["user"])

def get_user_service() -> IUserService:
    return get_container().resolve(IUserService)

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

@router.get("/me/profile", response_model=UserResponse)
async def get_current_user_profile(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return current_user

@router.put("/me/profile", response_model=UserResponse)
async def update_current_user_profile(
    data: UserCreate,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: IUserService = Depends(get_user_service)
):
    return await service.update_user(current_user.id, data)