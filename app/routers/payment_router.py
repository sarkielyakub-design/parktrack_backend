from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.shipment_model import Shipment

router = APIRouter(prefix="/payment")


# ✅ save payment


@router.post("/pay")
def pay(
    data: dict = Body(...),
    db: Session = Depends(get_db),
):

    tracking = data["tracking_id"]

    method = data["method"]

    ref = data.get("ref")

    s = db.query(Shipment).filter(
        Shipment.tracking_id == tracking
    ).first()

    if not s:
        return {"error": "not found"}

    s.paid = True

    s.payment_method = method

    s.payment_ref = ref

    db.commit()

    return {"msg": "paid"}


# ✅ revenue


@router.get("/revenue")
def revenue(db: Session = Depends(get_db)):

    s = db.query(Shipment).all()

    total = sum([x.price for x in s])

    paid = sum([x.price for x in s if x.paid])

    unpaid = total - paid

    return {

        "total": total,

        "paid": paid,

        "unpaid": unpaid,

        "count": len(s),

    }