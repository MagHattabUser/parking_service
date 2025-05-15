from sqlalchemy.future import select

from domain.i_car import ICar
from infrastructure.repositories.base import BaseRepository
from domain.models import Car

class CarRepository(BaseRepository, ICar):
    async def get_by_number(self, number: str):
        async with self.db.get_session() as session:
            result = await session.execute(select(Car).where(Car.number == number))
        return result.scalars().first()