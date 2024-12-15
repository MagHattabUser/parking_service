from repositories.parking_place import ParkingPlaceRepository
from models import ParkingPlace
from schemas import ParkingPlaceCreate
from fastapi import HTTPException

class PlaceService:
    def __init__(self, place_repo: ParkingPlaceRepository):
        self.place_repo = place_repo

    async def get_places_by_zone(self, zona_identifier: str | int):
        return await self.place_repo.get_by_zone(zona_identifier)
    #mapper для преобразование из dto в entity и обратно
    async def create_place(self, place_data: ParkingPlaceCreate):
        place = ParkingPlace(**place_data.dict())
        return await self.place_repo.save(place)

    async def delete_place(self, place_id: int):
        place = await self.place_repo.delete_by_id(place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        return place
