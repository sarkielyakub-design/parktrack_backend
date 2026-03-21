from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.database.database import Base, engine, SessionLocal
from app.models.models import User

from app.routers.auth_router import router as auth_router
from app.routers.shipment_router import router as shipment_router
from app.routers.tracking_router import router as tracking_router
from app.routers.driver_router import router as driver_router
from fastapi.staticfiles import StaticFiles

from app.utils.hashing import get_password_hash


# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# CREATE ADMIN
# =========================

def create_admin():

    db: Session = SessionLocal()

    admin = db.query(User).filter(
        User.email == "admin@gmail.com"
    ).first()

    if not admin:

        hashed = get_password_hash("1234")

        new_admin = User(
            email="admin@gmail.com",
            password=hashed,
            role="admin"
        )

        db.add(new_admin)
        db.commit()

        print("Admin created")

    db.close()


create_admin()


# =========================
# APP
# =========================

app = FastAPI(
    title="ParkTrack API",
    version="0.1.0"
)
app.mount("/qr", StaticFiles(directory="qr_codes"), name="qr")
app.mount("/labels", StaticFiles(directory="labels"), name="labels")
app.mount("/barcodes", StaticFiles(directory="barcodes"), name="barcodes")

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTERS
# =========================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    shipment_router,
    prefix="/shipment",
    tags=["Shipment"]
)

app.include_router(
    tracking_router,
    prefix="/tracking",
    tags=["Tracking"]
)

app.include_router(
    driver_router,
    prefix="/driver",
    tags=["Driver"]
)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "msg": "ParkTrack API running"
    }