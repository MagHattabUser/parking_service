from sqlalchemy.future import select

from domain.i_car_user import ICarUser
from infrastructure.repositories.base import BaseRepository
from domain.models import CarUser

class CarUserRepository(BaseRepository, ICarUser):
    async def list_by_user(self, user_id: int):
        """Все CarUser для данного User"""
        async with self.db.get_session() as session:
            result = await session.execute(select(CarUser).where(CarUser.user_id == user_id))
        return result.scalars().all()

    async def list_by_car(self, car_id: int):
        """Все CarUser для данной Car"""
        async with self.db.get_session() as session:
            result = await session.execute(select(CarUser).where(CarUser.car_id == car_id))
        return result.scalars().all()