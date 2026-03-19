from pydantic import BaseModel

class ShipmentCreate(BaseModel):
    tracking_id: str
    sender: str
    receiver: str
    origin: str
    destination: str
    status: str


class ShipmentResponse(BaseModel):
    tracking_id: str
    sender: str
    receiver: str
    origin: str
    destination: str
    status: str

    class Config:
        orm_mode = True