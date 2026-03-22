from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from database import get_db
from models.shipment_model import Shipment

router = APIRouter(prefix="/payment")


@router.post("/save")
def save_payment(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking = data.get("tracking_id")
    amount = data.get("amount")
    ref = data.get("ref")

    shipment = db.query(Shipment).filter(
        Shipment.tracking_id == tracking
    ).first()

    if not shipment:
        return {"error": "not found"}

    shipment.price = amount
    shipment.paid = True
    shipment.payment_ref = ref

    db.commit()

    return {"msg": "payment saved"}