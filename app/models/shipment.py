from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database.database import Base


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

    # ✅ PAYMENT

    price = Column(Float, default=0)

    paid = Column(Boolean, default=False)

    payment_method = Column(String, nullable=True)

    payment_ref = Column(String, nullable=True)