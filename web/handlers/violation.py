from fastapi import APIRouter, Depends
from typing import List

from web.container import get_container
from web.schemas import ViolationCreate, ViolationResponse
from application.services.interfaces.i_violation_service import IViolationService

router = APIRouter(prefix="/violation", tags=["violation"])

def get_violation_service() -> IViolationService:
    return get_container().resolve(IViolationService)

@router.post("/", response_model=ViolationResponse)
async def create_violation(data: ViolationCreate, service: IViolationService = Depends(get_violation_service)):
    return await service.create_violation(data)

@router.get("/{violation_id}", response_model=ViolationResponse)
async def get_violation(violation_id: int, service: IViolationService = Depends(get_violation_service)):
    return await service.get_violation(violation_id)

@router.get("/", response_model=List[ViolationResponse])
async def get_all_violations(service: IViolationService = Depends(get_violation_service)):
    return await service.get_all_violations()

@router.put("/{violation_id}", response_model=ViolationResponse)
async def update_violation(violation_id: int, data: ViolationCreate, service: IViolationService = Depends(get_violation_service)):
    return await service.update_violation(violation_id, data)

@router.delete("/{violation_id}")
async def delete_violation(violation_id: int, service: IViolationService = Depends(get_violation_service)):
    await service.delete_violation(violation_id)
    return {"message": "Violation deleted successfully"} 