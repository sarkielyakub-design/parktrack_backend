from sqlalchemy import Column, Integer, String
from app.database.database import Base
from sqlalchemy import Column, String, Float, DateTime

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True)
    sender = Column(String)
    receiver = Column(String)
    origin = Column(String)
    destination = Column(String)
    status = Column(String)
    barcode = Column(String, nullable=True)
    qr_code = Column(String, nullable=True)
    label_pdf = Column(String, nullable=True)
    proof_photo = Column(String, nullable=True)
    proof_sign = Column(String, nullable=True)
    delivered_lat = Column(Float, nullable=True)
    delivered_lng = Column(Float, nullable=True)
    confirmed_by = Column(String, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    price = Column(Float, default=0)
    payment_status = Column(String, default="pending")
    payment_method = Column(String, default="")