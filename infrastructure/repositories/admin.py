from typing import Optional

from sqlalchemy.future import select

from domain.i_admin import IAdmin
from infrastructure.repositories.base import BaseRepository
from domain.models import Admin

class AdminRepository(BaseRepository, IAdmin):
    async def get_by_name(self, admin_name: str) -> Optional[Admin]:
        async with self.db.get_session() as session:
            result = await session.execute(select(Admin).where(Admin.name == admin_name))
        return result.scalars().first()
        
    async def get_by_email(self, email: str) -> Optional[Admin]:
        async with self.db.get_session() as session:
            result = await session.execute(select(Admin).where(Admin.email == email))
            return result.scalars().first()
