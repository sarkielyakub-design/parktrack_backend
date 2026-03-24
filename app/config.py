import os

BASE_DIR = os.getcwd()

LABEL_DIR = os.path.join(BASE_DIR, "labels")
QR_DIR = os.path.join(BASE_DIR, "qr_codes")
BARCODE_DIR = os.path.join(BASE_DIR, "barcodes")

os.makedirs(LABEL_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)
os.makedirs(BARCODE_DIR, exist_ok=True)