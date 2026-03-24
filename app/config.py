import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

LABEL_DIR = os.path.join(ROOT_DIR, "labels")
QR_DIR = os.path.join(ROOT_DIR, "qr_codes")
BARCODE_DIR = os.path.join(ROOT_DIR, "barcodes")

os.makedirs(LABEL_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)
os.makedirs(BARCODE_DIR, exist_ok=True)