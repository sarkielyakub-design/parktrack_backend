
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
)

from datetime import datetime

from app.database.database import Base


# ================= USER =================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True)

    password = Column(String)

    role = Column(String, default="user")


# ================= DRIVER =================

class Driver(Base):

    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String)

    status = Column(String, default="idle")

# ================= HISTORY =================

class ShipmentHistory(Base):

    __tablename__ = "shipment_history"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(
        Integer,
        ForeignKey("shipments.id"),
    )

    tracking_id = Column(String)

    status = Column(String)

    location = Column(String)

    lat = Column(Float)

    lng = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# ================= DRIVER LOCATION =================

class DriverLocation(Base):

    __tablename__ = "driver_locations"

    id = Column(Integer, primary_key=True, index=True)

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
    )

    lat = Column(Float)

    lng = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )