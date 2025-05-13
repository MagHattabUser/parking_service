from datetime import datetime
from typing import List
from web.schemas import ViolationCreate, ViolationResponse
from application.services.interfaces.i_violation_service import IViolationService
from infrastructure.repositories.violation import ViolationRepository
from web.mapper import ViolationMapper
from domain.models import Violation

class ViolationService(IViolationService):
    def __init__(self, violation_repo: ViolationRepository):
        self.violation_repo = violation_repo
        self.mapper = ViolationMapper()

    async def list_by_place(self, place_id: int) -> List[ViolationResponse]:
        violations = await self.violation_repo.list_by_place(place_id)
        return [self.mapper.to_response(violation) for violation in violations]

    async def list_by_date_range(self, start: datetime, end: datetime) -> List[ViolationResponse]:
        violations = await self.violation_repo.list_by_date_range(start, end)
        return [self.mapper.to_response(violation) for violation in violations]

    async def create_violation(self, data: ViolationCreate) -> ViolationResponse:
        violation = self.mapper.to_entity(data)
        created_violation = await self.violation_repo.save(violation)
        return self.mapper.to_response(created_violation)

    async def get_violation(self, violation_id: int) -> ViolationResponse:
        violation = await self.violation_repo.get_by_id(Violation, violation_id)
        if not violation:
            raise ValueError(f"Violation with id {violation_id} not found")
        return self.mapper.to_response(violation)

    async def get_all_violations(self) -> List[ViolationResponse]:
        violations = await self.violation_repo.get_by_all(Violation)
        return [self.mapper.to_response(violation) for violation in violations]

    async def update_violation(self, violation_id: int, data: ViolationCreate) -> ViolationResponse:
        violation = await self.violation_repo.get_by_id(Violation, violation_id)
        if not violation:
            raise ValueError(f"Violation with id {violation_id} not found")
        
        updated_violation = self.mapper.to_entity(data)
        updated_violation.id = violation_id
        
        updated_violation = await self.violation_repo.update(updated_violation)
        return self.mapper.to_response(updated_violation)

    async def delete_violation(self, violation_id: int) -> None:
        violation = await self.violation_repo.get_by_id(Violation, violation_id)
        if not violation:
            raise ValueError(f"Violation with id {violation_id} not found")
        await self.violation_repo.delete(violation) 