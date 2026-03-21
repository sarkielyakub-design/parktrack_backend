from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
import os


LABEL_FOLDER = "labels"

os.makedirs(LABEL_FOLDER, exist_ok=True)


def generate_label(
    shipment,
    qr_path,
    barcode_path,
):

    file_path = f"{LABEL_FOLDER}/{shipment.tracking_id}.pdf"

    c = canvas.Canvas(
        file_path,
        pagesize=A6
    )

    c.setFont("Helvetica", 10)

    c.drawString(10, 380, "ZTECHTRACKIA")

    c.drawString(
        10,
        360,
        f"Tracking: {shipment.tracking_id}",
    )

    c.drawString(
        10,
        340,
        f"Sender: {shipment.sender_name}",
    )

    c.drawString(
        10,
        320,
        f"Receiver: {shipment.receiver_name}",
    )

    c.drawString(
        10,
        300,
        f"Phone: {shipment.receiver_phone}",
    )

    c.drawString(
        10,
        280,
        f"From: {shipment.from_city}",
    )

    c.drawString(
        10,
        260,
        f"To: {shipment.to_city}",
    )

    # QR

    if qr_path:
        c.drawImage(
            qr_path,
            200,
            260,
            width=100,
            height=100,
        )

    # BARCODE

    if barcode_path:
        c.drawImage(
            barcode_path,
            50,
            200,
            width=200,
            height=50,
        )

    c.save()

    return file_path