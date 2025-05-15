from datetime import datetime, timedelta
from typing import Annotated, Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from domain.models import User, Admin
from web.schemas import TokenData
from web.config import Configs

oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="auth/token/admin")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="auth/token/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_config() -> Configs:
    from web.container import get_container
    return get_container().resolve(Configs)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
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
    configs = get_config()
    
    try:
        payload = jwt.decode(token, configs.JWT_SECRET_KEY, algorithms=[configs.JWT_ALGORITHM])
        
        if return_payload:
            return payload
            
        email: str = payload.get("sub")
        if email is None:
            return None
            
        token_data = TokenData(
            email=email,
            role=payload.get("role"),
            subject_id=payload.get("subject_id")
        )
        return token_data
    except JWTError:
        return None
