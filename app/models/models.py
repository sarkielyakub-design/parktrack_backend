
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


# ================= SHIPMENT =================





class Shipment(Base):

    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

    tracking_id = Column(String, unique=True)

    status = Column(String)

    location = Column(String)

    sender_name = Column(String)
    sender_phone = Column(String)

    receiver_name = Column(String)
    receiver_phone = Column(String)

    from_city = Column(String)
    to_city = Column(String)

    note = Column(String)

    otp = Column(String)

    qr_code = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    label_pdf = Column(String, nullable=True)

    delivered_lat = Column(Float, nullable=True)
    delivered_lng = Column(Float, nullable=True)

    delivered_at = Column(DateTime, nullable=True)

    confirmed_by = Column(String, nullable=True)

    proof_photo = Column(String, nullable=True)
    proof_sign = Column(String, nullable=True)

    # ✅ PAYMENT
    price = Column(Float, default=0)

    payment_status = Column(String, default="pending")

    payment_method = Column(String, default="")

    payment_ref = Column(String, nullable=True)
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