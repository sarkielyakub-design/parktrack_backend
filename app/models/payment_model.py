from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    tracking_id = Column(String)

    amount = Column(Float)

    method = Column(String)

    ref = Column(String)