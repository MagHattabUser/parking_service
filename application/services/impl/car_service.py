from typing import List
from web.schemas import CarCreate, CarResponse
from application.services.interfaces.i_car_service import ICarService
from infrastructure.repositories.car import CarRepository
from web.mapper import CarMapper
from domain.models import Car

class CarService(ICarService):
    def __init__(self, car_repo: CarRepository):
        self.car_repo = car_repo
        self.mapper = CarMapper()

    async def create_car(self, data: CarCreate) -> CarResponse:
        car = self.mapper.to_entity(data)
        created_car = await self.car_repo.save(car)
        return self.mapper.to_response(created_car)

    async def get_car(self, car_id: int) -> CarResponse:
        car = await self.car_repo.get_by_id(Car, car_id)
        if not car:
            raise ValueError(f"Car with id {car_id} not found")
        return self.mapper.to_response(car)

    async def get_all_cars(self) -> List[CarResponse]:
        cars = await self.car_repo.get_by_all(Car)
        return [self.mapper.to_response(car) for car in cars]

    async def update_car(self, car_id: int, data: CarCreate) -> CarResponse:
        car = await self.car_repo.get_by_id(Car, car_id)
        if not car:
            raise ValueError(f"Car with id {car_id} not found")
        
        updated_car = self.mapper.to_entity(data)
        updated_car.id = car_id
        
        updated_car = await self.car_repo.update(updated_car)
        return self.mapper.to_response(updated_car)

    async def delete_car(self, car_id: int) -> None:
        car = await self.car_repo.get_by_id(Car, car_id)
        if not car:
            raise ValueError(f"Car with id {car_id} not found")
        await self.car_repo.delete(car) 