from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Any
from datetime import datetime, time
import re

class UserBase(BaseModel):
    user_name: str
    phone: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'\d', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None
    subject_id: int | None = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class CarBase(BaseModel):
    car_number: str

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

    class Config:
        orm_mode = True

class CarUserBase(BaseModel):
    user_id: int
    car_id: int

class CarUserCreate(CarUserBase):
    pass

class CarUserResponse(CarUserBase):
    id: int

    class Config:
        orm_mode = True

class BookingStatusBase(BaseModel):
    status_name: str

class BookingStatusCreate(BookingStatusBase):
    pass

class BookingStatusResponse(BookingStatusBase):
    id: int

    class Config:
        orm_mode = True

class PlaceStatusBase(BaseModel):
    status_name: str

class PlaceStatusCreate(PlaceStatusBase):
    pass

class PlaceStatusResponse(PlaceStatusBase):
    id: int

    class Config:
        orm_mode = True

class ZoneTypeBase(BaseModel):
    type_name: str

class ZoneTypeCreate(ZoneTypeBase):
    pass

class ZoneTypeResponse(ZoneTypeBase):
    id: int

    class Config:
        orm_mode = True

class AdminBase(BaseModel):
    admin_name: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'\d', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

class AdminResponse(AdminBase):
    id: int

    class Config:
        orm_mode = True
        
class Admin(AdminBase):
    id: int
    
    class Config:
        from_attributes = True

type Coordinates = List[List[float]]
class ParkingZoneBase(BaseModel):
    zone_name: str
    zone_type_id: int
    address: str
    start_time: time
    end_time: time
    price_per_minute: int
    location: Any  # JSONB field
    update_time: datetime
    admin_id: int

class ParkingZoneCreate(ParkingZoneBase):
    pass

class ParkingZoneResponse(ParkingZoneBase):
    id: int

    class Config:
        orm_mode = True

class CameraBase(BaseModel):
    camera_name: str
    url: str
    parking_zone_id: int

class CameraCreate(CameraBase):
    pass

class CameraResponse(CameraBase):
    id: int

    class Config:
        orm_mode = True

type JSONCoords = Any
class CameraParkingPlaceBase(BaseModel):
    camera_id: int
    parking_place_id: int
    location: Any

class CameraParkingPlaceCreate(CameraParkingPlaceBase):
    pass

class CameraParkingPlaceResponse(CameraParkingPlaceBase):
    id: int

    class Config:
        orm_mode = True

class ParkingPlaceBase(BaseModel):
    place_number: int
    place_status_id: int
    parking_zone_id: int

class ParkingPlaceCreate(ParkingPlaceBase):
    pass

class ParkingPlaceResponse(ParkingPlaceBase):
    id: int

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    car_user_id: int
    start_time: datetime
    end_time: datetime
    parking_place_id: int
    booking_status_id: int

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int

    class Config:
        orm_mode = True

class ViolationBase(BaseModel):
    car_number: str
    timestamp: datetime
    parking_place_id: int

class ViolationCreate(ViolationBase):
    pass

class ViolationResponse(ViolationBase):
    id: int

    class Config:
        orm_mode = True

def validate_password_common(password):
    if len(password) < 8:
        raise ValueError('Пароль должен содержать минимум 8 символов')
    if not re.search(r'[A-Z]', password):
        raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
    if not re.search(r'[a-z]', password):
        raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
    if not re.search(r'\d', password):
        raise ValueError('Пароль должен содержать хотя бы одну цифру')
    return password

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password(cls, v):
        return validate_password_common(v)

class AdminLogin(UserLogin):
    pass
