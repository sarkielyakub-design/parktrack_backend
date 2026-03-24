from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from app.database.database import Base, engine, SessionLocal
from app.models.models import User

from app.routers.auth_router import router as auth_router
from app.routers.shipment_router import router as shipment_router
from app.routers.tracking_router import router as tracking_router
from app.routers.driver_router import router as driver_router
from app.routers.payment_router import router as payment_router

from app.utils.hashing import get_password_hash

import os


# =========================
# BASE DIR (SAFE FOR RENDER)
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LABEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "labels"))
QR_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "qr_codes"))
BARCODE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "barcodes"))
PROOF_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "proof"))
SIGN_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "sign"))


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
    version="3.0"
)


# =========================
# CREATE FOLDERS
# =========================

os.makedirs(LABEL_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)
os.makedirs(BARCODE_DIR, exist_ok=True)
os.makedirs(PROOF_DIR, exist_ok=True)
os.makedirs(SIGN_DIR, exist_ok=True)


# =========================
# STATIC FILES
# =========================

app.mount(
    "/labels",
    StaticFiles(directory=LABEL_DIR),
    name="labels",
)

app.mount(
    "/qr",
    StaticFiles(directory=QR_DIR),
    name="qr",
)

app.mount(
    "/barcodes",
    StaticFiles(directory=BARCODE_DIR),
    name="barcodes",
)

app.mount(
    "/proof",
    StaticFiles(directory=PROOF_DIR),
    name="proof",
)

app.mount(
    "/sign",
    StaticFiles(directory=SIGN_DIR),
    name="sign",
)


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

app.include_router(auth_router, prefix="/auth")
app.include_router(shipment_router, prefix="/shipment")
app.include_router(tracking_router, prefix="/tracking")
app.include_router(driver_router, prefix="/driver")
app.include_router(payment_router, prefix="/payment")


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"msg": "ParkTrack API running"}