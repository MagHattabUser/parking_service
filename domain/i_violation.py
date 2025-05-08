from typing import List, Optional
from datetime import datetime
from domain.models import Violation
from domain.i_base import IBase
from abc import abstractmethod

class IViolation(IBase):
    @abstractmethod
    async def list_by_place(self, place_id: int) -> List[Violation]:
        """Все нарушения для конкретного места"""
        pass

    @abstractmethod
    async def list_by_date_range(self, start: datetime, end: datetime) -> List[Violation]:
        """Фильтрация нарушений по временным диапазонам"""
        pass