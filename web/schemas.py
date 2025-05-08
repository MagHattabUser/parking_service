from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime, time

# User
class UserBase(BaseModel):
    user_name: str
    phone: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Car
class CarBase(BaseModel):
    car_number: str

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

    class Config:
        orm_mode = True

# CarUser (association)
class CarUserBase(BaseModel):
    user_id: int
    car_id: int

class CarUserCreate(CarUserBase):
    pass

class CarUserResponse(CarUserBase):
    id: int

    class Config:
        orm_mode = True

# BookingStatus
class BookingStatusBase(BaseModel):
    status_name: str

class BookingStatusCreate(BookingStatusBase):
    pass

class BookingStatusResponse(BookingStatusBase):
    id: int

    class Config:
        orm_mode = True

# PlaceStatus
class PlaceStatusBase(BaseModel):
    status_name: str

class PlaceStatusCreate(PlaceStatusBase):
    pass

class PlaceStatusResponse(PlaceStatusBase):
    id: int

    class Config:
        orm_mode = True

# ZoneType
class ZoneTypeBase(BaseModel):
    type_name: str

class ZoneTypeCreate(ZoneTypeBase):
    pass

class ZoneTypeResponse(ZoneTypeBase):
    id: int

    class Config:
        orm_mode = True

# Admin
class AdminBase(BaseModel):
    admin_name: str
    email: str

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int

    class Config:
        orm_mode = True

# ParkingZone
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

# Camera
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

# CameraParkingPlace
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

# ParkingPlace
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

# Booking
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

# Violation
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
