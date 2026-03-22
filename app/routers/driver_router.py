from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.shipment import Shipment
from app.models.models import ShipmentHistory
from app.models.models import Driver, DriverLocation
router = APIRouter()


# =========================
# MODELS
# =========================

class DriverCreate(BaseModel):
    name: str
    phone: str


class DriverLogin(BaseModel):
    phone: str


class DriverUpdate(BaseModel):
    name: str
    phone: str
    status: str


class LocationSend(BaseModel):
    driver_id: int
    lat: float
    lng: float


class AssignDriver(BaseModel):
    driver_id: int


# =========================
# CREATE DRIVER
# =========================

@router.post("/create")
def create_driver(
    data: DriverCreate,
    db: Session = Depends(get_db),
):

    d = Driver(
        name=data.name,
        phone=data.phone,
        status="idle",
    )

    db.add(d)
    db.commit()

    return {"msg": "driver created"}


# =========================
# GET ALL
# =========================

@router.get("/all")
def get_drivers(
    db: Session = Depends(get_db),
):

    return db.query(Driver).all()


# =========================
# WITH LOCATION
# =========================

@router.get("/with-location")
def drivers_with_location(
    db: Session = Depends(get_db),
):

    drivers = db.query(Driver).all()

    result = []

    for d in drivers:

        loc = (
            db.query(DriverLocation)
            .filter(
                DriverLocation.driver_id == d.id
            )
            .order_by(
                DriverLocation.id.desc()
            )
            .first()
        )

        shipment = (
            db.query(Shipment)
            .filter(
                Shipment.driver_id == d.id
            )
            .first()
        )

        result.append({

            "id": d.id,
            "name": d.name,
            "status": d.status,

            "lat": loc.lat if loc else 0,
            "lng": loc.lng if loc else 0,

            "tracking_id":
                shipment.tracking_id
                if shipment else None,
        })

    return result


# =========================
# LOGIN
# =========================

@router.post("/login")
def driver_login(
    data: DriverLogin,
    db: Session = Depends(get_db),
):

    d = db.query(Driver).filter(
        Driver.phone == data.phone
    ).first()

    if not d:
        raise HTTPException(404)

    return {
        "id": d.id,
        "name": d.name,
        "status": d.status,
    }


# =========================
# DELETE
# =========================

@router.delete("/delete/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
):

    d = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not d:
        raise HTTPException(404)

    db.delete(d)
    db.commit()

    return {"msg": "deleted"}


# =========================
# UPDATE
# =========================

@router.put("/update/{driver_id}")
def update_driver(
    driver_id: int,
    data: DriverUpdate,
    db: Session = Depends(get_db),
):

    d = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not d:
        raise HTTPException(404)

    d.name = data.name
    d.phone = data.phone
    d.status = data.status

    db.commit()

    return {"msg": "updated"}


# =========================
# SEND LOCATION
# =========================

@router.post("/send-location")
def send_location(
    data: LocationSend,
    db: Session = Depends(get_db),
):

    loc = DriverLocation(
        driver_id=data.driver_id,
        lat=data.lat,
        lng=data.lng,
    )

    db.add(loc)
    db.commit()

    shipment = db.query(Shipment).filter(
        Shipment.driver_id == data.driver_id
    ).first()

    if not shipment:
        return {"msg": "location saved"}

    # safe status change

    if shipment.status == "created":
        shipment.status = "in transit"

    elif shipment.status == "in transit":
        shipment.status = "out for delivery"

    history = ShipmentHistory(

        shipment_id=shipment.id,
        tracking_id=shipment.tracking_id,

        status=shipment.status,

        location="GPS",

        lat=data.lat,
        lng=data.lng,
    )

    db.add(history)
    db.commit()

    return {"msg": "updated"}


