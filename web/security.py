from datetime import datetime, timedelta
from typing import Annotated, Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from domain.models import User, Admin
from web.schemas import TokenData
from web.config import Configs

# Определяем схемы OAuth2 для пользователя и администратора
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="auth/token/admin")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="auth/token/user")

# Оставляем для обратной совместимости
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_config() -> Configs:
    """Получить конфигурацию с использованием отложенного импорта"""
    from web.container import get_container
    return get_container().resolve(Configs)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка соответствия пароля хэшу"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Получение хэша пароля"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT токена доступа"""
    configs = get_config()
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=configs.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, configs.JWT_SECRET_KEY, algorithm=configs.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, return_payload: bool = False) -> Optional[TokenData] | dict:
    """Проверка JWT токена и извлечение данных
    
    Args:
        token: JWT токен для проверки
        return_payload: Если True, возвращает полный payload вместо TokenData
        
    Returns:
        TokenData или полный payload в зависимости от return_payload
    """
    configs = get_config()
    
    try:
        payload = jwt.decode(token, configs.JWT_SECRET_KEY, algorithms=[configs.JWT_ALGORITHM])
        
        if return_payload:
            return payload
            
        email: str = payload.get("sub")
        if email is None:
            return None
            
        # Создаем TokenData с дополнительными полями для роли и ID
        token_data = TokenData(
            email=email,
            role=payload.get("role"),
            subject_id=payload.get("subject_id")
        )
        return token_data
    except JWTError:
        return None


# Функции ниже оставлены для обратной совместимости.
# Рекомендуется использовать функции из unified_auth.py: 
# get_current_user, get_current_admin, get_current_user_or_admin

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Получение текущего аутентифицированного пользователя по JWT токену (устаревшая)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Проверяем токен
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    # Проверяем роль
    if token_data.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для доступа"
        )

    # Получаем пользователя из базы данных
    from web.container import get_container
    from application.services.interfaces.i_unified_auth_service import IUnifiedAuthService
    auth_service = get_container().resolve(IUnifiedAuthService)
    user = await auth_service.get_by_email(token_data.email, "user")
    
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)]) -> Admin:
    """Получение текущего аутентифицированного администратора по JWT токену (устаревшая)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Проверяем токен
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    # Проверяем роль
    if token_data.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для доступа"
        )

    # Получаем администратора из базы данных
    from web.container import get_container
    from application.services.interfaces.i_unified_auth_service import IUnifiedAuthService
    auth_service = get_container().resolve(IUnifiedAuthService)
    admin = await auth_service.get_by_email(token_data.email, "admin")
    
    if admin is None:
        raise credentials_exception
    return admin


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Получение активного пользователя с возможностью дополнительных проверок"""
    # Здесь можно добавить проверку, активен ли пользователь, например:
    # if hasattr(current_user, 'is_active') and not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Пользователь неактивен")
    return current_user
