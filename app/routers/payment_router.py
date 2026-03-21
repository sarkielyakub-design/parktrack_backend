from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.payment_model import Payment
from app.models.shipment_model import Shipment


router = APIRouter(prefix="/payment")


# ✅ save payment


@router.post("/save")

def save_payment(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking = data["tracking_id"]

    amount = data["amount"]

    ref = data["ref"]


    p = Payment(

        tracking_id=tracking,

        amount=amount,

        method="paystack",

        ref=ref,

    )

    db.add(p)


    # mark shipment paid

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking
    ).first()

    if s:

        s.paid = True

        s.payment_ref = ref


    db.commit()

    return {"msg": "paid"}