import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

Base = declarative_base()

class ParkingZone(Base):
    __tablename__ = 'parking_zones'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    coordinates = Column(JSON, nullable=False)

    parking_places = relationship("ParkingPlace", back_populates="zone")


class ParkingPlace(Base):
    __tablename__ = 'parking_places'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    zone_id = Column(Integer, ForeignKey('parking_zones.id'), nullable=False)

    zone = relationship("ParkingZone", back_populates="parking_places")

#
# DATABASE_URL = "sqlite+aiosqlite:///./parking.db"
#
# engine = create_async_engine(DATABASE_URL, echo=True)
#
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# asyncio.run(create_tables())
