from typing import List
from web.schemas import CarUserCreate, CarUserResponse
from application.services.interfaces.i_car_user_service import ICarUserService
from infrastructure.repositories.car_user import CarUserRepository
from web.mapper import CarUserMapper
from domain.models import CarUser

class CarUserService(ICarUserService):
    def __init__(self, car_user_repo: CarUserRepository):
        self.car_user_repo = car_user_repo
        self.mapper = CarUserMapper()

    async def assign_car(self, data: CarUserCreate) -> CarUserResponse:
        car_user = self.mapper.to_entity(data)
        created_car_user = await self.car_user_repo.save(car_user)
        return self.mapper.to_response(created_car_user)

    async def unassign_car(self, car_user_id: int) -> None:
        car_user = await self.car_user_repo.get_by_id(CarUser, car_user_id)
        if not car_user:
            raise ValueError(f"CarUser with id {car_user_id} not found")
        await self.car_user_repo.delete(car_user)

    async def list_by_user(self, user_id: int) -> List[CarUserResponse]:
        car_users = await self.car_user_repo.list_by_user(user_id)
        return [self.mapper.to_response(car_user) for car_user in car_users]

    async def list_by_car(self, car_id: int) -> List[CarUserResponse]:
        car_users = await self.car_user_repo.list_by_car(car_id)
        return [self.mapper.to_response(car_user) for car_user in car_users]

    async def create_car_user(self, data: CarUserCreate) -> CarUserResponse:
        car_user = self.mapper.to_entity(data)
        created_car_user = await self.car_user_repo.save(car_user)
        return self.mapper.to_response(created_car_user)

    async def get_car_user(self, car_user_id: int) -> CarUserResponse:
        car_user = await self.car_user_repo.get_by_id(CarUser, car_user_id)
        if not car_user:
            raise ValueError(f"CarUser with id {car_user_id} not found")
        return self.mapper.to_response(car_user)

    async def get_all_car_users(self) -> List[CarUserResponse]:
        car_users = await self.car_user_repo.get_by_all(CarUser)
        return [self.mapper.to_response(car_user) for car_user in car_users]

    async def update_car_user(self, car_user_id: int, data: CarUserCreate) -> CarUserResponse:
        car_user = await self.car_user_repo.get_by_id(CarUser, car_user_id)
        if not car_user:
            raise ValueError(f"CarUser with id {car_user_id} not found")
        
        updated_car_user = self.mapper.to_entity(data)
        updated_car_user.id = car_user_id
        
        updated_car_user = await self.car_user_repo.update(updated_car_user)
        return self.mapper.to_response(updated_car_user)

    async def delete_car_user(self, car_user_id: int) -> None:
        car_user = await self.car_user_repo.get_by_id(CarUser, car_user_id)
        if not car_user:
            raise ValueError(f"CarUser with id {car_user_id} not found")
        await self.car_user_repo.delete(car_user) 