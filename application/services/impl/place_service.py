from infrastructure.repositories.parking_place import ParkingPlaceRepository
from web.schemas import ParkingPlaceCreate
from fastapi import HTTPException
from web.mapper import ParkingPlaceMapper
from application.services.i_place_service import IPlaceService


class PlaceService(IPlaceService):
    def __init__(self, place_repo: ParkingPlaceRepository):
        self.place_repo = place_repo

    async def get_places_by_zone(self, zona_identifier: str | int):
        return await self.place_repo.get_by_zone(zona_identifier)

    async def create_place(self, place_data: ParkingPlaceCreate):
        place = ParkingPlaceMapper.to_entity(place_data)
        return await self.place_repo.save(place)

    async def delete_place(self, place_id: int):
        place = await self.place_repo.delete_by_id(place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        return place
