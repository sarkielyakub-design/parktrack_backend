import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_label(shipment, qr_path, barcode_path):

    os.makedirs("labels", exist_ok=True)

    filename = f"{shipment.tracking_id}.pdf"

    file_path = os.path.join(
        "labels",
        filename
    )

    # ✅ FIX PATHS

    qr_real = qr_path.replace("/", "", 1) if qr_path.startswith("/") else qr_path
    barcode_real = barcode_path.replace("/", "", 1) if barcode_path.startswith("/") else barcode_path

    c = canvas.Canvas(
        file_path,
        pagesize=letter
    )

    # HEADER

    c.setFillColorRGB(1, 1, 0)
    c.rect(0, 700, 600, 80, fill=1)

    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 18)

    c.drawString(
        50,
        740,
        "ZTECHTRACKIA EXPRESS"
    )

    # TRACKING

    c.setFont("Helvetica-Bold", 22)

    c.drawString(
        50,
        680,
        shipment.tracking_id
    )

    # INFO

    c.setFont("Helvetica", 12)

    c.drawString(50, 650, f"FROM: {shipment.from_city}")
    c.drawString(50, 630, f"TO: {shipment.to_city}")
    c.drawString(50, 610, f"Receiver: {shipment.receiver_name}")
    c.drawString(50, 590, f"Phone: {shipment.receiver_phone}")
    c.drawString(50, 570, f"Sender: {shipment.sender_name}")

    # BARCODE

    if os.path.exists(barcode_real):

        c.drawImage(
            barcode_real,
            50,
            480,
            width=300,
            height=80
        )

    else:
        print("BARCODE NOT FOUND:", barcode_real)

    # QR

    if os.path.exists(qr_real):

        c.drawImage(
            qr_real,
            400,
            480,
            width=120,
            height=120
        )

    else:
        print("QR NOT FOUND:", qr_real)

    c.save()

    return f"/labels/{filename}"