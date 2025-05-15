from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Union, Any
from datetime import datetime, timedelta
import secrets

from domain.i_unified_auth import IUnifiedAuth
from domain.models import User, Admin, RefreshToken, AdminRefreshToken
from infrastructure.repositories.base import BaseRepository
from web.security import verify_password
from web.config import Configs


class UnifiedAuthRepository(BaseRepository, IUnifiedAuth):
    async def verify_credentials(self, email: str, password: str, role: str) -> Optional[Union[User, Admin]]:
        async with self.db.get_session() as session:
            model = User if role == "user" else Admin
            
            result = await session.execute(select(model).where(model.email == email))
            subject = result.scalars().first()
            
            if not subject:
                return None
                
            if not verify_password(password, subject.password):
                return None
                
            return subject
    
    async def save_refresh_token(self, subject_id: int, role: str, token: str = None) -> str:
        if token is None:
            token = secrets.token_hex(32)
        
        configs = Configs()
        expires_delta = timedelta(days=configs.REFRESH_TOKEN_EXPIRE_DAYS)
        expires_at = datetime.utcnow() + expires_delta
        
        if role == "user":
            model = RefreshToken
            new_token = RefreshToken(
                user_id=subject_id,
                token=token,
                expires_at=expires_at,
                created_at=datetime.utcnow()
            )
            fk_column = RefreshToken.user_id == subject_id
        else:
            model = AdminRefreshToken
            new_token = AdminRefreshToken(
                admin_id=subject_id,
                token=token,
                expires_at=expires_at,
                created_at=datetime.utcnow()
            )
            fk_column = AdminRefreshToken.admin_id == subject_id
        
        async with self.db.get_session() as session:
            await session.execute(
                delete(model).where(fk_column)
            )
            session.add(new_token)
            await session.commit()
            
        return token
    
    async def get_refresh_token(self, subject_id: int, role: str) -> Optional[str]:
        async with self.db.get_session() as session:
            if role == "user":
                model = RefreshToken
                fk_column = RefreshToken.user_id == subject_id
                order_column = RefreshToken.created_at.desc()
            else:
                model = AdminRefreshToken
                fk_column = AdminRefreshToken.admin_id == subject_id
                order_column = AdminRefreshToken.created_at.desc()
            
            result = await session.execute(
                select(model)
                .where(fk_column)
                .where(model.expires_at > datetime.utcnow())
                .order_by(order_column)
            )
            token_record = result.scalars().first()
            
            if not token_record:
                return None
                
            return token_record.token
    
    async def validate_refresh_token(self, subject_id: int, role: str, token: str) -> bool:
        async with self.db.get_session() as session:
            if role == "user":
                model = RefreshToken
                fk_column = RefreshToken.user_id == subject_id
            else:
                model = AdminRefreshToken
                fk_column = AdminRefreshToken.admin_id == subject_id
            
            result = await session.execute(
                select(model)
                .where(fk_column)
                .where(model.token == token)
                .where(model.expires_at > datetime.utcnow())
            )
            token_record = result.scalars().first()
            
            return token_record is not None
    
    async def invalidate_refresh_token(self, subject_id: int, role: str) -> None:
        async with self.db.get_session() as session:
            if role == "user":
                model = RefreshToken
                fk_column = RefreshToken.user_id == subject_id
            else:
                model = AdminRefreshToken
                fk_column = AdminRefreshToken.admin_id == subject_id
            
            await session.execute(
                delete(model).where(fk_column)
            )
            await session.commit()
