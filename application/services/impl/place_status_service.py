from typing import List
from web.schemas import PlaceStatusCreate, PlaceStatusResponse
from application.services.interfaces.i_place_status_service import IPlaceStatusService
from infrastructure.repositories.place_status import PlaceStatusRepository
from web.mapper import PlaceStatusMapper
from domain.models import PlaceStatus

class PlaceStatusService(IPlaceStatusService):
    def __init__(self, place_status_repo: PlaceStatusRepository):
        self.place_status_repo = place_status_repo
        self.mapper = PlaceStatusMapper()

    async def list_all_statuses(self) -> List[PlaceStatusResponse]:
        statuses = await self.place_status_repo.get_by_all(PlaceStatus)
        return [self.mapper.to_response(status) for status in statuses]

    async def create_place_status(self, data: PlaceStatusCreate) -> PlaceStatusResponse:
        place_status = self.mapper.to_entity(data)
        created_place_status = await self.place_status_repo.save(place_status)
        return self.mapper.to_response(created_place_status)

    async def get_place_status(self, place_status_id: int) -> PlaceStatusResponse:
        place_status = await self.place_status_repo.get_by_id(PlaceStatus, place_status_id)
        if not place_status:
            raise ValueError(f"PlaceStatus with id {place_status_id} not found")
        return self.mapper.to_response(place_status)

    async def update_place_status(self, place_status_id: int, data: PlaceStatusCreate) -> PlaceStatusResponse:
        place_status = await self.place_status_repo.get_by_id(PlaceStatus, place_status_id)
        if not place_status:
            raise ValueError(f"PlaceStatus with id {place_status_id} not found")
        
        updated_place_status = self.mapper.to_entity(data)
        updated_place_status.id = place_status_id
        
        updated_place_status = await self.place_status_repo.update(updated_place_status)
        return self.mapper.to_response(updated_place_status)

    async def delete_place_status(self, place_status_id: int) -> None:
        place_status = await self.place_status_repo.get_by_id(PlaceStatus, place_status_id)
        if not place_status:
            raise ValueError(f"PlaceStatus with id {place_status_id} not found")
        await self.place_status_repo.delete(place_status) 