from typing import List
from infrastructure.repositories.parking_place import ParkingPlaceRepository
from web.schemas import ParkingPlaceCreate, ParkingPlaceResponse
from web.mapper import ParkingPlaceMapper
from application.services.interfaces.i_parking_place_service import IParkingPlaceService
from domain.models import ParkingPlace
from web.schemas import ParkingPlaceResponse # Ensure ParkingPlaceResponse is imported if not already

class ParkingPlaceService(IParkingPlaceService):
    def __init__(self, parking_place_repo: ParkingPlaceRepository):
        self.parking_place_repo = parking_place_repo
        self.mapper = ParkingPlaceMapper()

    async def list_by_zone(self, zone_id: int) -> List[ParkingPlaceResponse]:
        places = await self.parking_place_repo.list_by_zone(zone_id)
        return [self.mapper.to_response(place) for place in places]

    async def list_by_status(self, status_id: int) -> List[ParkingPlaceResponse]:
        places = await self.parking_place_repo.list_by_status(status_id)
        return [self.mapper.to_response(place) for place in places]

    async def get_places_by_zone(self, zone_id: int):
        return await self.parking_place_repo.list_by_zone(zone_id)

    async def create_place(self, data: ParkingPlaceCreate) -> ParkingPlaceResponse:
        place = self.mapper.to_entity(data)
        created_place = await self.parking_place_repo.save(place)
        return self.mapper.to_response(created_place)

    async def get_place(self, place_id: int) -> ParkingPlaceResponse:
        place = await self.parking_place_repo.get_by_id(ParkingPlace, place_id)
        if not place:
            raise ValueError(f"Parking place with id {place_id} not found")
        return self.mapper.to_response(place)

    async def get_all_places(self) -> List[ParkingPlaceResponse]:
        places = await self.parking_place_repo.get_by_all(ParkingPlace)
        return [self.mapper.to_response(place) for place in places]

    async def update_place(self, place_id: int, data: ParkingPlaceCreate) -> ParkingPlaceResponse:
        place = await self.parking_place_repo.get_by_id(ParkingPlace, place_id)
        if not place:
            raise ValueError(f"Parking place with id {place_id} not found")
        
        updated_place = self.mapper.to_entity(data)
        updated_place.id = place_id
        
        updated_place = await self.parking_place_repo.update(updated_place)
        return self.mapper.to_response(updated_place)

    async def delete_place(self, place_id: int) -> None:
        place = await self.parking_place_repo.get_by_id(ParkingPlace, place_id)
        if not place:
            raise ValueError(f"Parking place with id {place_id} not found")
        await self.parking_place_repo.delete(place)

    async def update_place_status(self, place_id: int, status_id: int) -> ParkingPlaceResponse:
        place = await self.parking_place_repo.get_by_id(ParkingPlace, place_id)
        if not place:
            raise ValueError(f"Parking place with id {place_id} not found")
        
        place.place_status_id = status_id
        updated_place_entity = await self.parking_place_repo.update(place) # Assuming repo.update() takes the entity and returns it
        return self.mapper.to_response(updated_place_entity)
