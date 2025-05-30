from sqlalchemy.future import select

from domain.i_user import IUser
from infrastructure.repositories.base import BaseRepository
from domain.models import User

class UserRepository(BaseRepository, IUser):
    async def get_by_phone(self, phone: str):
        async with self.db.get_session() as session:
            result = await session.execute(select(User).where(User.phone == phone))
        return result.scalars().first()

    async def get_by_email(self, email: str):
        async with self.db.get_session() as session:
            result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, username: str):
        async with self.db.get_session() as session:
            result = await session.execute(select(User).where(User.username == username))
        return result.scalars().first()