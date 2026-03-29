from app.models.shipment import Shipment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sqlalchemy import text

import os

from app.database.database import Base, engine, SessionLocal
from app.models.models import User

from app.routers.auth_router import router as auth_router
from app.routers.shipment_router import router as shipment_router
from app.routers.tracking_router import router as tracking_router
from app.routers.driver_router import router as driver_router
from app.routers.payment_router import router as payment_router

from app.utils.hashing import get_password_hash
from app.websocket.socket import websocket_endpoint




# =========================
# CREATE APP FIRST ✅
# =========================

app = FastAPI(
    title="ParkTrack API",
    version="4.0"
)


# =========================
# CORS (ONLY ONCE)
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.websocket("/ws/{tracking_id}")(websocket_endpoint)
# =========================
# BASE DIR (RENDER SAFE)
# =========================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

LABEL_DIR = os.path.join(BASE_DIR, "labels")
QR_DIR = os.path.join(BASE_DIR, "qr_codes")
BARCODE_DIR = os.path.join(BASE_DIR, "barcodes")
PROOF_DIR = os.path.join(BASE_DIR, "proof")
SIGN_DIR = os.path.join(BASE_DIR, "sign")


print("BASE_DIR =", BASE_DIR)
print("QR_DIR =", QR_DIR)


# =========================
# CREATE TABLES
# =========================




Base.metadata.create_all(bind=engine)


# =========================
# FIX driver_id COLUMN
# =========================

try:
    with engine.connect() as conn:
        conn.execute(
            text(
                "ALTER TABLE shipments ADD COLUMN driver_id INTEGER"
            )
        )
        conn.commit()
        print("driver_id column added")
except Exception as e:
    print("driver_id exists or error:", e)


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
# ROUTERS
# =========================

app.include_router(auth_router, prefix="/auth")
app.include_router(shipment_router, prefix="/shipment")
app.include_router(tracking_router, prefix="/tracking")
app.include_router(driver_router, prefix="/driver")
app.include_router(payment_router, prefix="/payment")





def fix_columns():
    with engine.begin() as conn:  # ✅ IMPORTANT (AUTOCOMMIT)

        try:
            conn.execute(text("ALTER TABLE shipments ADD COLUMN pickup_lat FLOAT"))
        except Exception as e:
            print("pickup_lat exists:", e)

        try:
            conn.execute(text("ALTER TABLE shipments ADD COLUMN pickup_lng FLOAT"))
        except Exception as e:
            print("pickup_lng exists:", e)

        try:
            conn.execute(text("ALTER TABLE shipments ADD COLUMN drop_lat FLOAT"))
        except Exception as e:
            print("drop_lat exists:", e)

        try:
            conn.execute(text("ALTER TABLE shipments ADD COLUMN drop_lng FLOAT"))
        except Exception as e:
            
          print("drop_lng exists:", e)
        
        
        @app.on_event("startup")
        def startup_event():
         fix_columns()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"msg": "ParkTrack API running"}