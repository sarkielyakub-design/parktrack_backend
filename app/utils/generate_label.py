import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.config import LABEL_DIR


def generate_label(
    shipment,
    qr_path,
    barcode_path,
):

    path = os.path.join(
        LABEL_DIR,
        f"{shipment.tracking_id}.pdf"
    )

    c = canvas.Canvas(path, pagesize=letter)

    c.drawString(50, 750, "ZTECHTRACKIA EXPRESS")
    c.drawString(50, 720, shipment.tracking_id)

    if os.path.exists(barcode_path):
        c.drawImage(barcode_path, 50, 600, 250, 80)

    if os.path.exists(qr_path):
        c.drawImage(qr_path, 320, 600, 120, 120)

    c.save()

    print("LABEL SAVED:", path)

    return path