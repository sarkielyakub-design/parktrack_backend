import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = os.getcwd()


def generate_label(shipment, qr_path, barcode_path):

    folder = os.path.join(BASE_DIR, "labels")
    os.makedirs(folder, exist_ok=True)

    filename = f"{shipment.tracking_id}.pdf"

    path = os.path.join(folder, filename)

    c = canvas.Canvas(path, pagesize=letter)

    # HEADER
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "ZTECHTRACKIA EXPRESS")

    c.setFont("Helvetica", 12)

    c.drawString(50, 720, shipment.tracking_id)
    c.drawString(50, 700, shipment.from_city)
    c.drawString(50, 680, shipment.to_city)

    # barcode
    if os.path.exists(barcode_path):
        c.drawImage(barcode_path, 50, 560, 250, 80)

    # qr
    if os.path.exists(qr_path):
        c.drawImage(qr_path, 320, 560, 120, 120)

    c.save()

    return path