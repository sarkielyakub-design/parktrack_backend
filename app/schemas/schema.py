from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ShipmentCreate(BaseModel):
    tracking_id: str
    status: str
    location: str


class ShipmentUpdate(BaseModel):
    status: str
    location: str        

class HistoryCreate(BaseModel):
    tracking_id: str
    status: str
    location: str    