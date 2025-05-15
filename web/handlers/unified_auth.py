from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional, Union
from pydantic import BaseModel
from functools import partial

from domain.models import User, Admin
from web.schemas import UserCreate, AdminCreate, Token, User as UserSchema, Admin as AdminSchema, UserLogin, AdminLogin
from web.security import verify_token
from web.container import get_container
from application.services.interfaces.i_unified_auth_service import IUnifiedAuthService

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="auth/token/admin")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="auth/token/user")
oauth2_scheme = oauth2_scheme_admin


async def get_current_user_or_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    required_role: Optional[str] = None
) -> Union[User, Admin]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
        
    if required_role and token_data.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для доступа"
        )

    container = get_container()
    auth_service = container.resolve(IUnifiedAuthService)
    
    subject = await auth_service.get_by_email(token_data.email, token_data.role)
    if subject is None:
        raise credentials_exception
    return subject


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme_user)]) -> User:
    return await get_current_user_or_admin(token, required_role="user")

async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme_admin)]) -> Admin:
    return await get_current_user_or_admin(token, required_role="admin")


@router.post("/register/user", response_model=UserSchema, summary="Регистрация пользователя")
async def register_user(user_data: UserCreate):
    container = get_container()
    auth_service = container.resolve(IUnifiedAuthService)
    
    try:
        created_user = await auth_service.register(user_data, "user")
        return created_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/register/admin", response_model=AdminSchema, summary="Регистрация администратора")
async def register_admin(admin_data: AdminCreate):
    container = get_container()
    auth_service = container.resolve(IUnifiedAuthService)
    
    try:
        created_admin = await auth_service.register(admin_data, "admin")
        return created_admin
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token/user", response_model=Token, summary="Получение токена доступа пользователя")
async def login_user(login_data: UserLogin):
    try:
        container = get_container()
        auth_service = container.resolve(IUnifiedAuthService)

        subject = await auth_service.authenticate(login_data.email, login_data.password, "user")
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = await auth_service.create_token(subject, "user")
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token/admin", response_model=Token, summary="Получение токена доступа администратора")
async def login_admin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        container = get_container()
        auth_service = container.resolve(IUnifiedAuthService)
        
        subject = await auth_service.authenticate(form_data.username, form_data.password, "admin")
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = await auth_service.create_token(subject, "admin")
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=Union[UserSchema, AdminSchema], summary="Получение информации о текущем пользователе")
async def read_current_profile(current_subject: Annotated[Union[User, Admin], Depends(get_current_user_or_admin)]):
    return current_subject


@router.get("/user/me", response_model=UserSchema, summary="Получение информации о пользователе")
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/admin/me", response_model=AdminSchema, summary="Получение информации об администраторе")
async def read_admin_me(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    return current_admin


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Выход из системы")
async def logout(
    current_subject: Annotated[Union[User, Admin], Depends(get_current_user_or_admin)],
    response: Response,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    payload = verify_token(token, return_payload=True)
    role = payload.get("role", "user")
    
    container = get_container()
    auth_service = container.resolve(IUnifiedAuthService)
    
    await auth_service.logout(current_subject.id, role)
    
    response.delete_cookie(key="access_token")
    return None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    subject_id: int
    role: str


@router.post("/refresh", response_model=Token, summary="Обновление access токена")
async def refresh_token(refresh_data: RefreshTokenRequest):
    if refresh_data.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недопустимая роль. Используйте 'user' или 'admin'"
        )
        
    container = get_container()
    auth_service = container.resolve(IUnifiedAuthService)
    
    new_token = await auth_service.refresh_access_token(
        refresh_data.subject_id, refresh_data.role, refresh_data.refresh_token
    )
    
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return new_token
