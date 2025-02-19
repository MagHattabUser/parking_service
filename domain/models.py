from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class ParkingZone(Base):
    __tablename__ = 'parking_zones'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    coordinates = Column(JSONB, nullable=False)

    parking_places = relationship("ParkingPlace", back_populates="zone")


class ParkingPlace(Base):
    __tablename__ = 'parking_places'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    zone_id = Column(Integer, ForeignKey('parking_zones.id'), nullable=False)

    zone = relationship("ParkingZone", back_populates="parking_places")
