from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.shipment import Shipment

router = APIRouter(prefix="/payment")


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

    s.payment_status = "paid"
    s.payment_method = method
    s.payment_ref = ref

    db.commit()

    return {"msg": "paid"}


@router.get("/revenue")
def revenue(db: Session = Depends(get_db)):

    s = db.query(Shipment).all()

    total = sum([x.price for x in s])
    paid = sum([x.price for x in s if x.payment_status == "paid"])

    return {
        "total": total,
        "paid": paid,
        "unpaid": total - paid,
        "count": len(s),
    }