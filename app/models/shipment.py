from sqlalchemy import Column, Integer, String
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
    qr_code = Column(String, nullable=True)