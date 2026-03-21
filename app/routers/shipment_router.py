from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.qr_generator import generate_qr
import random
import string
from datetime import datetime
import requests

from app.database.database import get_db

from app.models.models import (
    Shipment,
    ShipmentHistory,
    Driver,
)

router = APIRouter()


# =========================
# MODELS
# =========================

class ConfirmDelivery(BaseModel):
    tracking_id: str
    otp: str
    name: str


class SendOtp(BaseModel):
    tracking_id: str


class AssignDriver(BaseModel):
    driver_id: int


# =========================
# HELPERS
# =========================

TERMII_KEY = "TLjHRGDHthHjfXVHwaORNFOHAvdZXfdjMHlQCaYFENHXRSDzfdqQjqVRBHSKeh"


def generate_tracking():
    return "ZT" + "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(8)
    )


def generate_otp():
    return str(random.randint(1000, 9999))


def send_sms(phone, message):
    print("SMS:", phone, message)
    return True


def send_whatsapp(phone, message):

    url = "https://api.ng.termii.com/api/sms/send"

    payload = {
        "to": phone,
        "from": "ZTECH",
        "sms": message,
        "type": "plain",
        "channel": "whatsapp",
        "api_key": TERMII_KEY,
    }

    requests.post(url, json=payload)

    return True


# =========================
# CREATE
# =========================

@router.post("/create")
def create_shipment(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking_id = generate_tracking()
    otp = generate_otp()

    shipment = Shipment(

        tracking_id=tracking_id,
        status="created",
        location=data.get("location"),

        sender_name=data.get("sender_name"),
        sender_phone=data.get("sender_phone"),

        receiver_name=data.get("receiver_name"),
        receiver_phone=data.get("receiver_phone"),

        from_city=data.get("from_city"),
        to_city=data.get("to_city"),

        note=data.get("note"),

        otp=otp,
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    history = ShipmentHistory(
        shipment_id=shipment.id,
        tracking_id=tracking_id,
        status="created",
        location=data.get("location"),
        lat=data.get("lat"),
        lng=data.get("lng"),
    )

    db.add(history)
    db.commit()

    return {
        "tracking_id": tracking_id,
        "otp": otp,
    }
qr_data = f"""
Tracking: {shipment.tracking_number}
Sender: {shipment.sender_name}
Receiver: {shipment.receiver_name}
Phone: {shipment.receiver_phone}
Destination: {shipment.destination}
"""

qr_path = generate_qr(
    qr_data,
    shipment.tracking_number
)

shipment.qr_code = qr_path

db.commit()
db.refresh(shipment)

# =========================
# UPDATE
# =========================

@router.put("/update/{tracking_id}")
def update_shipment(
    tracking_id: str,
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not s:
        raise HTTPException(404)

    s.status = data.get("status")
    s.location = data.get("location")

    if s.status == "out for delivery" and not s.otp:
        s.otp = generate_otp()

    db.commit()

    history = ShipmentHistory(
        shipment_id=s.id,
        tracking_id=tracking_id,
        status=s.status,
        location=s.location,
        lat=data.get("lat"),
        lng=data.get("lng"),
    )

    db.add(history)
    db.commit()

    return {"msg": "updated"}


# =========================
# TRACK
# =========================

@router.get("/track/{tracking_id}")
def track_shipment(
    tracking_id: str,
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not s:
        raise HTTPException(404)

    return s


# =========================
# ALL
# =========================

@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    return db.query(Shipment).all()


# =========================
# ASSIGN DRIVER
# =========================

@router.put("/assign-driver/{tracking_id}")
def assign_driver(
    tracking_id: str,
    data: AssignDriver,
    db: Session = Depends(get_db),
):

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not shipment:
        raise HTTPException(404, "Shipment not found")

    driver = db.query(Driver).filter(
        Driver.id == data.driver_id
    ).first()

    if not driver:
        raise HTTPException(404, "Driver not found")

    shipment.driver_id = data.driver_id

    db.commit()

    return {
        "msg": "driver assigned",
        "tracking_id": tracking_id,
        "driver_id": data.driver_id,
    }


# =========================
# CONFIRM DELIVERY
# =========================

@router.post("/confirm-delivery")
def confirm_delivery(
    data: ConfirmDelivery,
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == data.tracking_id
    ).first()

    if not s:
        raise HTTPException(404)

    if str(s.otp) != str(data.otp):
        raise HTTPException(400, "Wrong OTP")

    s.status = "delivered"
    s.confirmed_by = data.name
    s.delivered = 1
    s.delivered_at = datetime.utcnow()

    db.commit()

    history = ShipmentHistory(
        shipment_id=s.id,
        tracking_id=s.tracking_id,
        status="delivered",
        location=s.to_city,
        lat=0,
        lng=0,
    )

    db.add(history)
    db.commit()

    return {"msg": "Delivered confirmed"}


# =========================
# SEND OTP SMS
# =========================

@router.post("/send-otp")
def send_otp(
    data: SendOtp,
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == data.tracking_id
    ).first()

    if not s:
        raise HTTPException(404)

    if not s.otp:
        s.otp = generate_otp()

    message = f"""
ZTECHTRACKIA
Tracking: {s.tracking_id}
OTP: {s.otp}
"""

    send_sms(s.receiver_phone, message)

    db.commit()

    return {"msg": "OTP sent"}


# =========================
# SEND OTP WHATSAPP
# =========================

@router.post("/send-otp-whatsapp")
def send_otp_whatsapp(
    data: SendOtp,
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == data.tracking_id
    ).first()

    if not s:
        raise HTTPException(404)

    message = f"""
ZTECHTRACKIA
Tracking: {s.tracking_id}
OTP: {s.otp}
"""

    send_whatsapp(s.receiver_phone, message)

    return {"msg": "WhatsApp OTP sent"}
from fastapi import UploadFile, File


@router.post("/save-proof/{tracking_id}")
def save_proof(
    tracking_id: str,
    name: str = "",
    qr: str = "",
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not s:
        raise HTTPException(404)

    s.confirmed_by = name
    s.proof_qr = qr

    db.commit()

    return {"msg": "proof saved"}
@router.post("/save-photo/{tracking_id}")
def save_photo(
    tracking_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    path = f"photos/{tracking_id}.jpg"

    with open(path, "wb") as f:
        f.write(file.file.read())

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    s.proof_photo = path

    db.commit()

    return {"msg": "photo saved"}
@router.post("/save-signature/{tracking_id}")
def save_signature(
    tracking_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    path = f"sign/{tracking_id}.png"

    with open(path, "wb") as f:
        f.write(file.file.read())

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    s.proof_signature = path

    db.commit()

    return {"msg": "signature saved"}
@router.get("/shipment/{shipment_id}/label")
def get_label(shipment_id: int, db: Session = Depends(get_db)):

    shipment = db.query(Shipment).get(shipment_id)

    if not shipment:
        return {"error": "Not found"}

    return {
        "tracking": shipment.tracking_number,
        "qr": shipment.qr_code
    }