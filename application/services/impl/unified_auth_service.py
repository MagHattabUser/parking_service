from datetime import  timedelta
from typing import Optional, Union, Dict, Any

from domain.models import User, Admin
from web.schemas import Token, UserCreate, AdminCreate
from domain.i_unified_auth import IUnifiedAuth
from domain.i_user import IUser
from domain.i_admin import IAdmin
from application.services.interfaces.i_unified_auth_service import IUnifiedAuthService
from web.security import get_password_hash, create_access_token
from web.config import Configs


class UnifiedAuthService(IUnifiedAuthService):
    def __init__(self,
                 unified_auth_repository: IUnifiedAuth,
                 user_repository: IUser,
                 admin_repository: IAdmin):
        self.auth_repository = unified_auth_repository
        self.user_repository = user_repository
        self.admin_repository = admin_repository

    async def register(self, data: Union[UserCreate, AdminCreate], role: str) -> Union[User, Admin]:
        email = data.email

        if role == "user":
            existing_user = await self.user_repository.get_by_email(email)
            if existing_user:
                raise ValueError("Email уже зарегистрирован")

            existing_phone = await self.user_repository.get_by_phone(data.phone)
            if existing_phone:
                raise ValueError("Номер телефона уже зарегистрирован")

            hashed_password = get_password_hash(data.password)
            user = User(
                user_name=data.user_name,
                email=data.email,
                phone=data.phone,
                password=hashed_password
            )
            return await self.user_repository.save(user)
        else:
            existing_admin = await self.admin_repository.get_by_email(email)
            if existing_admin:
                raise ValueError("Email уже зарегистрирован")

            hashed_password = get_password_hash(data.password)
            admin = Admin(
                admin_name=data.admin_name,
                email=data.email,
                password=hashed_password
            )
            return await self.admin_repository.save(admin)

    async def authenticate(self, email: str, password: str, role: str) -> Optional[Union[User, Admin]]:
        """Аутентификация пользователя или администратора по email и паролю"""
        return await self.auth_repository.verify_credentials(email, password, role)

    async def create_token(self, subject: Union[User, Admin], role: str) -> Token:
        """Создание JWT токена и refresh токена"""
        subject_id = subject.id

        configs = Configs()
        access_token_expires = timedelta(minutes=configs.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        refresh_token = await self.auth_repository.save_refresh_token(subject_id, role)

        token_data: Dict[str, Any] = {
            "sub": subject.email,
            "role": role,
            "subject_id": subject_id
        }

        access_token = create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token
        )

    async def get_by_email(self, email: str, role: str) -> Optional[Union[User, Admin]]:
        if role == "user":
            return await self.user_repository.get_by_email(email)
        else:
            return await self.admin_repository.get_by_email(email)

    async def logout(self, subject_id: int, role: str) -> None:
        await self.auth_repository.invalidate_refresh_token(subject_id, role)

    async def refresh_access_token(self, subject_id: int, role: str, refresh_token: str) -> Optional[Token]:
        if not await self.auth_repository.validate_refresh_token(subject_id, role, refresh_token):
            return None

        subject = None
        if role == "user":
            subject = await self.user_repository.get_by_id(User, subject_id)
        else:
            subject = await self.admin_repository.get_by_id(Admin, subject_id)

        if not subject:
            return None

        return await self.create_token(subject, role)
