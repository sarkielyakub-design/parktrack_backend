from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.shipment_model import Shipment

router = APIRouter(prefix="/payment")


@router.post("/save")
def save_payment(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking = data.get("tracking_id")
    amount = data.get("amount")
    ref = data.get("ref")

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking
    ).first()

    if not s:
        return {"error": "not found"}

    s.price = amount
    s.paid = True
    s.payment_ref = ref

    db.commit()

    return {"msg": "payment saved"}