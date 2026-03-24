from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.generate_qr import generate_qr
import random
import string
from datetime import datetime
import requests
from app.utils.generate_label import generate_label
from app.utils.generate_barcode import generate_barcode
from app.database.database import get_db
from fastapi import UploadFile, File, Form
import shutil
import os
from datetime import datetime
from app.models.shipment import Shipment



from app.models.models import (
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
        price=data.get("price", 0),

        payment_status="pending",
        payment_method="",
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    # HISTORY

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

    # QR

    qr_file = generate_qr(
        tracking_id,
        tracking_id
    )

    # BARCODE

    barcode_file = generate_barcode(
        tracking_id
    )

    # LABEL

    label_file = generate_label(
        shipment,
        qr_file,
        barcode_file,
    )

    # URL

    qr_url = f"/qr/{tracking_id}.png"
    barcode_url = f"/barcodes/{tracking_id}.png"
    label_url = f"/labels/{tracking_id}.pdf"

    shipment.qr_code = qr_url
    shipment.barcode = barcode_url
    shipment.label_pdf = label_url

    db.commit()
    db.refresh(shipment)

    print("QR:", qr_file)
    print("BARCODE:", barcode_file)
    print("LABEL:", label_file)

    return {
        "tracking_id": tracking_id,
        "qr": qr_url,
        "barcode": barcode_url,
        "label": label_url,
        "otp": otp,
        "price": shipment.price,
    }
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
    db: Session = Depends(get_db)
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not s:
        return {}

    driver_data = None

    if hasattr(s, "driver_id") and s.driver_id:

        d = db.query(Driver).filter(
            Driver.id == s.driver_id
        ).first()

        if d:
            driver_data = {
                "name": d.name,
                "phone": d.phone,
            }

    return {

        "tracking_id": s.tracking_id,

        "status": s.status,

        "sender_name": s.sender_name,

        "receiver_name": s.receiver_name,

        "receiver_phone": s.receiver_phone,

        "from_city": s.from_city,

        "to_city": s.to_city,

        "note": s.note,

        "price": s.price,

        "driver": driver_data,
    }
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

    shipment = db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()

    if not shipment:
        return {"error": "Not found"}

    return {
        "id": shipment.id,
        "tracking_id": shipment.tracking_id,
        "qr": shipment.qr_code,
        "barcode": shipment.barcode,
        "label": shipment.label_pdf,
    }
@router.get("/barcode/{tracking_id}")
def track_by_barcode(
    tracking_id: str,
    db: Session = Depends(get_db),
):

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="Not found",
        )

    return shipment
@router.post("/confirm/by-scan")
def confirm_by_scan(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking_id = data.get("tracking_id")
    otp = data.get("otp")

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    if shipment.otp != otp:
        raise HTTPException(
            status_code=400,
            detail="Wrong OTP"
        )

    shipment.status = "delivered"
    shipment.delivered = True
    shipment.otp_verified = True

    db.commit()
    db.refresh(shipment)

    return {
        "msg": "Delivered",
        "tracking_id": tracking_id,
    }
@router.post("/confirm/proof")
def confirm_with_proof(

    tracking_id: str = Form(...),
    otp: str = Form(...),
    driver: str = Form(...),

    lat: float = Form(...),
    lng: float = Form(...),

    photo: UploadFile = File(...),
    sign: UploadFile = File(...),

    db: Session = Depends(get_db),

):

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not shipment:
        raise HTTPException(404)

    if shipment.otp != otp:
        raise HTTPException(400, "Wrong OTP")

    # ---------- save photo ----------

    os.makedirs("proof", exist_ok=True)

    photo_path = f"proof/{tracking_id}.jpg"

    with open(photo_path, "wb") as f:
        shutil.copyfileobj(
            photo.file,
            f,
        )

    # ---------- save sign ----------

    os.makedirs("sign", exist_ok=True)

    sign_path = f"sign/{tracking_id}.png"

    with open(sign_path, "wb") as f:
        shutil.copyfileobj(
            sign.file,
            f,
        )

    # ---------- update ----------

    shipment.status = "delivered"

    shipment.proof_photo = photo_path
    shipment.proof_sign = sign_path

    shipment.delivered_lat = lat
    shipment.delivered_lng = lng

    shipment.confirmed_by = driver
    shipment.delivered_at = datetime.utcnow()

    db.commit()
    db.refresh(shipment)

    return {"msg": "Delivered"}
@router.delete("/delete/{tracking_id}")
def delete_shipment(
    tracking_id: str,
    db: Session = Depends(get_db),
):

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not s:
        return {"msg": "not found"}

    # history
    db.query(ShipmentHistory).filter(
        ShipmentHistory.shipment_id == s.id
    ).delete()

    # delete shipment
    db.delete(s)

    db.commit()

    return {"msg": "deleted"}
@router.post("/confirm-by-qr")
def confirm_by_qr(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking_id = data.get("tracking_id")
    otp = data.get("otp")

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not shipment:
        return {"msg": "Shipment not found"}

    if shipment.otp != otp:
        return {"msg": "Wrong OTP"}

    shipment.status = "delivered"
    shipment.delivered = 1
    shipment.delivered_at = datetime.utcnow()

    db.commit()
    db.refresh(shipment)

    # ✅ history
    history = ShipmentHistory(
        shipment_id=shipment.id,
        tracking_id=tracking_id,
        status="delivered",
        location=shipment.location,
    )

    db.add(history)
    db.commit()

    return {
        "msg": "Delivered",
        "tracking": tracking_id,
    }
@router.post("/confirm/pro")
def confirm_pro(
    tracking_id: str = Form(...),
    otp: str = Form(...),
    driver: str = Form(...),
    lat: str = Form(...),
    lng: str = Form(...),

    photo: UploadFile = File(...),
    sign: UploadFile = File(...),

    db: Session = Depends(get_db),
):

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking_id
    ).first()

    if not shipment:
        return {"msg": "not found"}

    if shipment.otp != otp:
        return {"msg": "wrong otp"}

    # ✅ save photo
    os.makedirs("proof", exist_ok=True)

    photo_path = f"proof/{tracking_id}.jpg"

    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # ✅ save sign
    os.makedirs("sign", exist_ok=True)

    sign_path = f"sign/{tracking_id}.png"

    with open(sign_path, "wb") as buffer:
        shutil.copyfileobj(sign.file, buffer)

    # ✅ update shipment

    shipment.status = "delivered"
    shipment.delivered = 1
    shipment.confirmed_by = driver
    shipment.delivered_at = datetime.utcnow()

    shipment.proof_photo = photo_path
    shipment.signature = sign_path

    db.commit()
    db.refresh(shipment)

    # ✅ history

    history = ShipmentHistory(
        shipment_id=shipment.id,
        tracking_id=tracking_id,
        status="delivered",
        location=shipment.location,
        lat=lat,
        lng=lng,
    )

    db.add(history)
    db.commit()

    return {
        "msg": "DELIVERED",
        "tracking": tracking_id,
        "photo": photo_path,
        "sign": sign_path,
    }
@router.get("/timeline/{tracking_id}")
def timeline(
    tracking_id: str,
    db: Session = Depends(get_db),
):

    history = db.query(ShipmentHistory).filter(
        ShipmentHistory.tracking_id == tracking_id
    ).order_by(
        ShipmentHistory.id.desc()
    ).all()

    result = []

    for h in history:

        result.append({

            "status": h.status,
            "location": h.location,
            "lat": h.lat,
            "lng": h.lng,
            "time": str(h.created_at),

        })

    return result



@router.get("/last")
def get_last_shipment(db: Session = Depends(get_db)):

    s = db.query(Shipment).order_by(
        Shipment.id.desc()
    ).first()

    if not s:
        return {}

    driver_data = None

    if hasattr(s, "driver_id") and s.driver_id:

        d = db.query(Driver).filter(
            Driver.id == s.driver_id
        ).first()

        if d:
            driver_data = {
                "name": d.name,
                "phone": d.phone,
            }

    return {

        "tracking_id": s.tracking_id,

        "from_city": s.from_city,

        "to_city": s.to_city,

        "status": s.status,

        "driver": driver_data,
    }