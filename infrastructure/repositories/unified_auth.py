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
        """Проверка учетных данных пользователя или администратора"""
        async with self.db.get_session() as session:
            # Выбираем модель в зависимости от роли
            model = User if role == "user" else Admin
            
            # Ищем пользователя/администратора по email
            result = await session.execute(select(model).where(model.email == email))
            subject = result.scalars().first()
            
            if not subject:
                return None
                
            # Проверяем пароль
            if not verify_password(password, subject.password):
                return None
                
            return subject
    
    async def save_refresh_token(self, subject_id: int, role: str, token: str = None) -> str:
        """
        Сохранение токена обновления в базе данных.
        
        Args:
            subject_id: ID пользователя или администратора
            role: Роль ("user" или "admin")
            token: Токен (если None, будет сгенерирован)
        """
        # Если токен не предоставлен, генерируем новый
        if token is None:
            token = secrets.token_hex(32)  # 64-символьный токен
        
        # Вычисляем дату истечения срока действия
        configs = Configs()
        expires_delta = timedelta(days=configs.REFRESH_TOKEN_EXPIRE_DAYS)
        expires_at = datetime.utcnow() + expires_delta
        
        # Выбираем модель и создаем токен в зависимости от роли
        if role == "user":
            model = RefreshToken
            new_token = RefreshToken(
                user_id=subject_id,
                token=token,
                expires_at=expires_at,
                created_at=datetime.utcnow()
            )
            fk_column = RefreshToken.user_id == subject_id
        else:  # role == "admin"
            model = AdminRefreshToken
            new_token = AdminRefreshToken(
                admin_id=subject_id,
                token=token,
                expires_at=expires_at,
                created_at=datetime.utcnow()
            )
            fk_column = AdminRefreshToken.admin_id == subject_id
        
        async with self.db.get_session() as session:
            # Удаляем все существующие токены обновления для субъекта
            await session.execute(
                delete(model).where(fk_column)
            )
            # Сохраняем новый токен
            session.add(new_token)
            await session.commit()
            
        return token
    
    async def get_refresh_token(self, subject_id: int, role: str) -> Optional[str]:
        """Получение активного токена обновления"""
        async with self.db.get_session() as session:
            # Выбираем модель и условие в зависимости от роли
            if role == "user":
                model = RefreshToken
                fk_column = RefreshToken.user_id == subject_id
                order_column = RefreshToken.created_at.desc()
            else:  # role == "admin"
                model = AdminRefreshToken
                fk_column = AdminRefreshToken.admin_id == subject_id
                order_column = AdminRefreshToken.created_at.desc()
            
            # Находим актуальный (не истекший) токен
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
        """Проверка действительности токена обновления"""
        async with self.db.get_session() as session:
            # Выбираем модель и условие в зависимости от роли
            if role == "user":
                model = RefreshToken
                fk_column = RefreshToken.user_id == subject_id
            else:  # role == "admin"
                model = AdminRefreshToken
                fk_column = AdminRefreshToken.admin_id == subject_id
            
            # Проверяем наличие непросроченного токена
            result = await session.execute(
                select(model)
                .where(fk_column)
                .where(model.token == token)
                .where(model.expires_at > datetime.utcnow())
            )
            token_record = result.scalars().first()
            
            return token_record is not None
    
    async def invalidate_refresh_token(self, subject_id: int, role: str) -> None:
        """Инвалидация всех токенов обновления (выход из системы)"""
        async with self.db.get_session() as session:
            # Выбираем модель и условие в зависимости от роли
            if role == "user":
                model = RefreshToken
                fk_column = RefreshToken.user_id == subject_id
            else:  # role == "admin"
                model = AdminRefreshToken
                fk_column = AdminRefreshToken.admin_id == subject_id
            
            # Удаляем все токены субъекта
            await session.execute(
                delete(model).where(fk_column)
            )
            await session.commit()
