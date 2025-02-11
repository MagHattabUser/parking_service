from pydantic import BaseModel
from typing import List

class ParkingZoneBase(BaseModel):
    name: str
    coordinates: List[List[float]]

class ParkingZoneCreate(ParkingZoneBase):
    pass

class ParkingZoneResponse(ParkingZoneBase):
    id: int

    class Config:
        orm_mode = True


class ParkingPlaceBase(BaseModel):
    number: int

class ParkingPlaceCreate(ParkingPlaceBase):
    zone_id: int

class ParkingPlaceResponse(ParkingPlaceBase):
    id: int
    zone_id: int

    class Config:
        orm_mode = True
