import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_label(shipment, qr_path, barcode_path):

    folder = "labels"
    os.makedirs(folder, exist_ok=True)

    filename = f"{shipment.tracking_id}.pdf"

    path = os.path.join(folder, filename)

    c = canvas.Canvas(path, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "ZTECHTRACKIA EXPRESS")

    c.setFont("Helvetica", 12)

    c.drawString(50, 720, shipment.tracking_id)
    c.drawString(50, 700, shipment.from_city)
    c.drawString(50, 680, shipment.to_city)

    if os.path.exists(barcode_path):
        c.drawImage(barcode_path, 50, 550, 250, 80)

    if os.path.exists(qr_path):
        c.drawImage(qr_path, 320, 550, 120, 120)

    c.save()

    return path