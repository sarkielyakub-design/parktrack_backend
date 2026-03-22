from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def safe(v):
    if v is None:
        return ""
    return str(v)


def generate_label(
    shipment,
    qr_path,
    barcode_path,
):

    os.makedirs("labels", exist_ok=True)

    path = f"labels/{shipment.tracking_id}.pdf"

    c = canvas.Canvas(
        path,
        pagesize=letter,
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        750,
        f"Tracking: {safe(shipment.tracking_id)}",
    )

    c.drawString(
        50,
        730,
        f"Sender: {safe(shipment.sender_name)}",
    )

    c.drawString(
        50,
        710,
        f"Receiver: {safe(shipment.receiver_name)}",
    )

    c.drawString(
        50,
        690,
        f"From: {safe(shipment.from_city)}",
    )

    c.drawString(
        50,
        670,
        f"To: {safe(shipment.to_city)}",
    )

    c.drawString(
        50,
        650,
        f"Price: {safe(shipment.price)}",
    )

    c.drawString(
        50,
        630,
        f"Status: {safe(shipment.status)}",
    )

    # BARCODE
    try:
        if barcode_path:
            c.drawImage(
                barcode_path,
                50,
                520,
                width=250,
                height=80,
            )
    except:
        pass

    # QR
    try:
        if qr_path:
            c.drawImage(
                qr_path,
                320,
                520,
                width=120,
                height=120,
            )
    except:
        pass

    c.save()

    return path