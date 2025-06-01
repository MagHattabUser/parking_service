from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from domain.i_car_user import ICarUser
from infrastructure.repositories.base import BaseRepository
from domain.models import CarUser, Car

class CarUserRepository(BaseRepository, ICarUser):
    async def list_by_user(self, user_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(CarUser).where(CarUser.user_id == user_id))
        return result.scalars().all()

    async def list_by_car(self, car_id: int):
        async with self.db.get_session() as session:
            result = await session.execute(select(CarUser).where(CarUser.car_id == car_id))
        return result.scalars().all()
        
    async def get_detailed_by_user(self, user_id: int):
        async with self.db.get_session() as session:
            # Используем SQL запрос с JOIN для получения информации о машинах пользователя
            query = select(CarUser, Car.car_number).join(Car, CarUser.car_id == Car.id).where(CarUser.user_id == user_id)
            result = await session.execute(query)
            return result.all()