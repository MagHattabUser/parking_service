from typing import List
from web.schemas import ZoneTypeCreate, ZoneTypeResponse
from application.services.interfaces.i_zone_type_service import IZoneTypeService
from infrastructure.repositories.zone_type import ZoneTypeRepository
from web.mapper import ZoneTypeMapper
from domain.models import ZoneType

class ZoneTypeService(IZoneTypeService):
    def __init__(self, zone_type_repo: ZoneTypeRepository):
        self.zone_type_repo = zone_type_repo
        self.mapper = ZoneTypeMapper()

    async def list_all_types(self) -> List[ZoneTypeResponse]:
        types = await self.zone_type_repo.get_by_all(ZoneType)
        return [self.mapper.to_response(type_) for type_ in types]

    async def create_zone_type(self, data: ZoneTypeCreate) -> ZoneTypeResponse:
        zone_type = self.mapper.to_entity(data)
        created_zone_type = await self.zone_type_repo.save(zone_type)
        return self.mapper.to_response(created_zone_type)

    async def get_zone_type(self, zone_type_id: int) -> ZoneTypeResponse:
        zone_type = await self.zone_type_repo.get_by_id(ZoneType, zone_type_id)
        if not zone_type:
            raise ValueError(f"ZoneType with id {zone_type_id} not found")
        return self.mapper.to_response(zone_type)

    async def update_zone_type(self, zone_type_id: int, data: ZoneTypeCreate) -> ZoneTypeResponse:
        zone_type = await self.zone_type_repo.get_by_id(ZoneType, zone_type_id)
        if not zone_type:
            raise ValueError(f"ZoneType with id {zone_type_id} not found")
        
        updated_zone_type = self.mapper.to_entity(data)
        updated_zone_type.id = zone_type_id
        
        updated_zone_type = await self.zone_type_repo.update(updated_zone_type)
        return self.mapper.to_response(updated_zone_type)

    async def delete_zone_type(self, zone_type_id: int) -> None:
        zone_type = await self.zone_type_repo.get_by_id(ZoneType, zone_type_id)
        if not zone_type:
            raise ValueError(f"ZoneType with id {zone_type_id} not found")
        await self.zone_type_repo.delete(zone_type) 