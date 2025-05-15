from typing import List
from web.schemas import UserCreate, UserResponse
from application.services.interfaces.i_user_service import IUserService
from infrastructure.repositories.user import UserRepository
from web.mapper import UserMapper
from domain.models import User

class UserService(IUserService):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.mapper = UserMapper()

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.user_repo.get_by_id(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return self.mapper.to_response(user)

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.user_repo.get_by_all(User)
        return [self.mapper.to_response(user) for user in users]

    async def update_user(self, user_id: int, data: UserCreate) -> UserResponse:
        user = await self.user_repo.get_by_id(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        updated_user = self.mapper.to_entity(data)
        updated_user.id = user_id
        
        updated_user = await self.user_repo.update(updated_user)
        return self.mapper.to_response(updated_user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repo.get_by_id(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        await self.user_repo.delete(user)