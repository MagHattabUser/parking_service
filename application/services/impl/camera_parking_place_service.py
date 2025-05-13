from typing import List
from web.schemas import CameraParkingPlaceCreate, CameraParkingPlaceResponse
from application.services.interfaces.i_camera_parking_place_service import ICameraParkingPlaceService
from infrastructure.repositories.camera_parking_place import CameraParkingPlaceRepository
from fastapi import HTTPException
from web.mapper import CameraParkingPlaceMapper
from domain.models import CameraParkingPlace

class CameraParkingPlaceService(ICameraParkingPlaceService):
    async def create_link(self, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        self._validate_polygon(data.location)
        camera_parking_place = self.mapper.to_entity(data)
        created_link = await self.camera_parking_place_repo.save(camera_parking_place)
        return self.mapper.to_response(created_link)

    async def list_places_for_camera(self, camera_id: int) -> List[CameraParkingPlaceResponse]:
        links = await self.camera_parking_place_repo.list_places_by_camera(camera_id)
        return [self.mapper.to_response(link) for link in links]

    async def list_cameras_for_place(self, place_id: int) -> List[CameraParkingPlaceResponse]:
        links = await self.camera_parking_place_repo.list_cameras_by_place(place_id)
        return [self.mapper.to_response(link) for link in links]

    def __init__(self, camera_parking_place_repo: CameraParkingPlaceRepository):
        self.camera_parking_place_repo = camera_parking_place_repo
        self.mapper = CameraParkingPlaceMapper()

    def _validate_polygon(self, coordinates: List[List[float]]) -> None:
        if not coordinates or len(coordinates) < 3:
            raise HTTPException(status_code=400, detail="Polygon must have at least 3 points")
        if coordinates[0] != coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed (first and last points must be the same)")

    async def create_camera_parking_place(self, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        self._validate_polygon(data.location)
        camera_parking_place = self.mapper.to_entity(data)
        created_camera_parking_place = await self.camera_parking_place_repo.save(camera_parking_place)
        return self.mapper.to_response(created_camera_parking_place)

    async def get_camera_parking_place(self, camera_parking_place_id: int) -> CameraParkingPlaceResponse:
        camera_parking_place = await self.camera_parking_place_repo.get_by_id(CameraParkingPlace, camera_parking_place_id)
        if not camera_parking_place:
            raise ValueError(f"CameraParkingPlace with id {camera_parking_place_id} not found")
        return self.mapper.to_response(camera_parking_place)

    async def get_all_camera_parking_places(self) -> List[CameraParkingPlaceResponse]:
        camera_parking_places = await self.camera_parking_place_repo.get_by_all(CameraParkingPlace)
        return [self.mapper.to_response(camera_parking_place) for camera_parking_place in camera_parking_places]

    async def update_camera_parking_place(self, camera_parking_place_id: int, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        self._validate_polygon(data.location)
        camera_parking_place = await self.camera_parking_place_repo.get_by_id(CameraParkingPlace, camera_parking_place_id)
        if not camera_parking_place:
            raise ValueError(f"CameraParkingPlace with id {camera_parking_place_id} not found")
        
        updated_camera_parking_place = self.mapper.to_entity(data)
        updated_camera_parking_place.id = camera_parking_place_id
        
        updated_camera_parking_place = await self.camera_parking_place_repo.update(updated_camera_parking_place)
        return self.mapper.to_response(updated_camera_parking_place)

    async def delete_camera_parking_place(self, camera_parking_place_id: int) -> None:
        camera_parking_place = await self.camera_parking_place_repo.get_by_id(CameraParkingPlace, camera_parking_place_id)
        if not camera_parking_place:
            raise ValueError(f"CameraParkingPlace with id {camera_parking_place_id} not found")
        await self.camera_parking_place_repo.delete(camera_parking_place) 