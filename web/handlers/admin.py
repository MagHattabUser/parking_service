from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import AdminCreate, AdminResponse
from application.services.interfaces.i_admin_service import IAdminService

router = APIRouter(prefix="/admin", tags=["admin"])

def get_admin_service() -> IAdminService:
    return get_container().resolve(IAdminService)

@router.post("/", response_model=AdminResponse)
async def create_admin(data: AdminCreate, service: IAdminService = Depends(get_admin_service)):
    return await service.create_admin(data)

@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin(admin_id: int, service: IAdminService = Depends(get_admin_service)):
    return await service.get_admin(admin_id)

@router.get("/", response_model=List[AdminResponse])
async def get_all_admins(service: IAdminService = Depends(get_admin_service)):
    return await service.get_all_admins()

@router.put("/{admin_id}", response_model=AdminResponse)
async def update_admin(admin_id: int, data: AdminCreate, service: IAdminService = Depends(get_admin_service)):
    return await service.update_admin(admin_id, data)

@router.delete("/{admin_id}")
async def delete_admin(admin_id: int, service: IAdminService = Depends(get_admin_service)):
    await service.delete_admin(admin_id)
    return {"message": "Admin deleted successfully"} 