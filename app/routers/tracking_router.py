from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.shipment import Shipment
from app.models.models import ShipmentHistory

router = APIRouter()


# =========================
# HISTORY
# =========================
@router.get("/history/{tracking_id}")
def get_history(
    tracking_id: str,
    db: Session = Depends(get_db)
):

    history = db.query(ShipmentHistory).filter(
        ShipmentHistory.tracking_id == tracking_id
    ).order_by(
        ShipmentHistory.created_at.desc()
    ).all()

    return history

# =========================
# LAST LOCATION
# =========================

@router.get("/last/{tracking_id}")
def last_location(
    tracking_id: str,
    db: Session = Depends(get_db)
):

    last = db.query(ShipmentHistory).filter(
        ShipmentHistory.tracking_id == tracking_id
    ).order_by(
        ShipmentHistory.created_at.desc()
    ).first()

    if not last:
        raise HTTPException(
            status_code=404,
            detail="no data"
        )

    return last