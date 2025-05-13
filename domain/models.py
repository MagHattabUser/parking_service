from sqlalchemy import (Column, Integer, String, DateTime, Time, Float, ForeignKey)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    car_users = relationship("CarUser", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    car_number = Column(String, nullable=False)

    car_users = relationship("CarUser", back_populates="car")


class CarUser(Base):
    __tablename__ = "car_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)

    user = relationship("User", back_populates="car_users")
    car = relationship("Car", back_populates="car_users")
    bookings = relationship("Booking", back_populates="car_user")


class BookingStatus(Base):
    __tablename__ = "booking_statuses"

    id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String, nullable=False)

    bookings = relationship("Booking", back_populates="status")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    car_user_id = Column(Integer, ForeignKey("car_users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    parking_place_id = Column(Integer, ForeignKey("parking_places.id"), nullable=False)
    booking_status_id = Column(Integer, ForeignKey("booking_statuses.id"), nullable=False)

    car_user = relationship("CarUser", back_populates="bookings")
    status = relationship("BookingStatus", back_populates="bookings")
    parking_place = relationship("ParkingPlace", back_populates="bookings")


class PlaceStatus(Base):
    __tablename__ = "place_statuses"

    id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String, nullable=False)

    parking_places = relationship("ParkingPlace", back_populates="status")


class ZoneType(Base):
    __tablename__ = "zone_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, nullable=False)

    parking_zones = relationship("ParkingZone", back_populates="zone_type")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    parking_zones = relationship("ParkingZone", back_populates="admin")
    refresh_tokens = relationship("AdminRefreshToken", back_populates="admin", cascade="all, delete-orphan")


class ParkingZone(Base):
    __tablename__ = "parking_zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String, nullable=False)
    zone_type_id = Column(Integer, ForeignKey("zone_types.id"), nullable=False)
    address = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    price_per_minute = Column(Integer, nullable=False)
    location = Column(JSONB, nullable=True)
    update_time = Column(DateTime, nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)

    zone_type = relationship("ZoneType", back_populates="parking_zones")
    admin = relationship("Admin", back_populates="parking_zones")
    cameras = relationship("Camera", back_populates="parking_zone")
    parking_places = relationship("ParkingPlace", back_populates="parking_zone")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    camera_name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    parking_zone_id = Column(Integer, ForeignKey("parking_zones.id"), nullable=False)

    parking_zone = relationship("ParkingZone", back_populates="cameras")
    camera_places = relationship("CameraParkingPlace", back_populates="camera")


class CameraParkingPlace(Base):
    __tablename__ = "camera_parking_places"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    parking_place_id = Column(Integer, ForeignKey("parking_places.id"), nullable=False)
    location = Column(JSONB, nullable=True)

    camera = relationship("Camera", back_populates="camera_places")
    parking_place = relationship("ParkingPlace", back_populates="camera_places")


class ParkingPlace(Base):
    __tablename__ = "parking_places"

    id = Column(Integer, primary_key=True, index=True)
    place_number = Column(Integer, nullable=False)
    place_status_id = Column(Integer, ForeignKey("place_statuses.id"), nullable=False)
    parking_zone_id = Column(Integer, ForeignKey("parking_zones.id"), nullable=False)

    status = relationship("PlaceStatus", back_populates="parking_places")
    parking_zone = relationship("ParkingZone", back_populates="parking_places")
    camera_places = relationship("CameraParkingPlace", back_populates="parking_place")
    bookings = relationship("Booking", back_populates="parking_place")
    violations = relationship("Violation", back_populates="parking_place")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    car_number = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    parking_place_id = Column(Integer, ForeignKey("parking_places.id"), nullable=False)

    parking_place = relationship("ParkingPlace", back_populates="violations")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="refresh_tokens")


class AdminRefreshToken(Base):
    __tablename__ = "admin_refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    admin = relationship("Admin", back_populates="refresh_tokens")
