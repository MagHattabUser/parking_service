from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

from web.schemas import ViolationCreate, ViolationResponse

class IViolationService(ABC):
    @abstractmethod
    async def create_violation(self, data: ViolationCreate) -> ViolationResponse:
        pass

    @abstractmethod
    async def get_violation(self, violation_id: int) -> ViolationResponse:
        pass

    @abstractmethod
    async def list_by_place(self, place_id: int) -> List[ViolationResponse]:
        pass

    @abstractmethod
    async def list_by_date_range(self, start: datetime, end: datetime) -> List[ViolationResponse]:
        pass

    @abstractmethod
    async def get_all_violations(self) -> List[ViolationResponse]:
        pass

    @abstractmethod
    async def update_violation(self, violation_id: int, data: ViolationCreate) -> ViolationResponse:
        pass

    @abstractmethod
    async def delete_violation(self, violation_id: int) -> None:
        pass