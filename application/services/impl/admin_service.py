from typing import List
from web.schemas import AdminCreate, AdminResponse
from application.services.interfaces.i_admin_service import IAdminService
from infrastructure.repositories.admin import AdminRepository
from web.mapper import AdminMapper
from domain.models import Admin

class AdminService(IAdminService):
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo
        self.mapper = AdminMapper()

    async def create_admin(self, data: AdminCreate) -> AdminResponse:
        admin = self.mapper.to_entity(data)
        created_admin = await self.admin_repo.save(admin)
        return self.mapper.to_response(created_admin)

    async def get_admin(self, admin_id: int) -> AdminResponse:
        admin = await self.admin_repo.get_by_id(Admin, admin_id)
        if not admin:
            raise ValueError(f"Admin with id {admin_id} not found")
        return self.mapper.to_response(admin)

    async def get_all_admins(self) -> List[AdminResponse]:
        admins = await self.admin_repo.get_by_all(Admin)
        return [self.mapper.to_response(admin) for admin in admins]

    async def update_admin(self, admin_id: int, data: AdminCreate) -> AdminResponse:
        admin = await self.admin_repo.get_by_id(Admin, admin_id)
        if not admin:
            raise ValueError(f"Admin with id {admin_id} not found")
        
        updated_admin = self.mapper.to_entity(data)
        updated_admin.id = admin_id
        
        updated_admin = await self.admin_repo.save(updated_admin)
        return self.mapper.to_response(updated_admin)

    async def delete_admin(self, admin_id: int) -> None:
        admin = await self.admin_repo.get_by_id(Admin, admin_id)
        if not admin:
            raise ValueError(f"Admin with id {admin_id} not found")
        await self.admin_repo.delete(admin)