from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.database import Base


class Shipment(Base):

    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

    tracking_id = Column(String, unique=True)

    status = Column(String)
    location = Column(String)
    driver_id = Column(Integer, nullable=True)

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

    proof_photo = Column(String, nullable=True)
    proof_sign = Column(String, nullable=True)

    delivered_lat = Column(Float, nullable=True)
    delivered_lng = Column(Float, nullable=True)

    confirmed_by = Column(String, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    # ✅ payment
    price = Column(Float, default=0)
    payment_status = Column(String, default="pending")
    payment_method = Column(String, default="")
    payment_ref = Column(String, nullable=True)