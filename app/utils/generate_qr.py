import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = os.getcwd()

def generate_label(shipment, qr_path, barcode_path):

    folder = os.path.join(BASE_DIR, "labels")
    os.makedirs(folder, exist_ok=True)

    filename = f"{shipment.tracking_id}.pdf"

    path = os.path.join(folder, filename)

    print("LABEL SAVED:", path)

    c = canvas.Canvas(path, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "ZTECHTRACKIA EXPRESS")

    c.drawString(50, 720, shipment.tracking_id)

    if os.path.exists(barcode_path):
        c.drawImage(barcode_path, 50, 600, 250, 80)

    if os.path.exists(qr_path):
        c.drawImage(qr_path, 320, 600, 120, 120)

    c.save()

    return path