from abc import ABC, abstractmethod
from typing import List

from web.schemas import PlaceStatusResponse, PlaceStatusCreate


class IPlaceStatusService(ABC):
    @abstractmethod
    async def list_all_statuses(self) -> List[PlaceStatusResponse]:
        pass

    @abstractmethod
    async def create_place_status(self, data: PlaceStatusCreate) -> PlaceStatusResponse:
        pass

    @abstractmethod
    async def get_place_status(self, place_status_id: int) -> PlaceStatusResponse:
        pass

    @abstractmethod
    async def update_place_status(self, place_status_id: int, data: PlaceStatusCreate) -> PlaceStatusResponse:
        pass

    @abstractmethod
    async def delete_place_status(self, place_status_id: int) -> None:
        pass