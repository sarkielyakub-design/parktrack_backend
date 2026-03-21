import os

from reportlab.lib.pagesizes import mm
from reportlab.lib.colors import yellow, black
from reportlab.pdfgen import canvas

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
        pagesize=(100 * mm, 150 * mm),
    )

    width = 100 * mm
    height = 150 * mm

    # ================= BACKGROUND =================

    c.setFillColor(yellow)
    c.rect(
        0,
        height - 40,
        width,
        40,
        fill=1,
        stroke=0,
    )

    # ================= TITLE =================

    c.setFillColor(black)

    c.setFont(
        "Helvetica-Bold",
        14,
    )

    c.drawString(
        10,
        height - 25,
        "ZTECHTRACKIA EXPRESS",
    )

    # ================= TRACKING BIG =================

    c.setFont(
        "Helvetica-Bold",
        18,
    )

    c.drawString(
        10,
        height - 60,
        shipment.tracking_id,
    )

    y = height - 80

    # ================= FROM / TO =================

    c.setFont(
        "Helvetica",
        10,
    )

    c.drawString(
        10,
        y,
        f"FROM: {shipment.from_city}",
    )

    y -= 15

    c.drawString(
        10,
        y,
        f"TO: {shipment.to_city}",
    )

    y -= 20

    # ================= RECEIVER =================

    c.setFont(
        "Helvetica-Bold",
        11,
    )

    c.drawString(
        10,
        y,
        f"Receiver: {shipment.receiver_name}",
    )

    y -= 15

    c.setFont(
        "Helvetica",
        10,
    )

    c.drawString(
        10,
        y,
        f"Phone: {shipment.receiver_phone}",
    )

    y -= 20

    # ================= SENDER =================

    c.drawString(
        10,
        y,
        f"Sender: {shipment.sender_name}",
    )

    y -= 25

    # ================= BARCODE =================

    if os.path.exists(barcode_path):

        c.drawImage(
            barcode_path,
            10,
            y - 60,
            width=250,
            height=60,
        )

    y -= 70

    # ================= QR =================

    if os.path.exists(qr_path):

        c.drawImage(
            qr_path,
            width - 90,
            y - 80,
            width=80,
            height=80,
        )

    y -= 90

    # ================= FOOTER =================

    c.setFont(
        "Helvetica",
        8,
    )

    c.drawString(
        10,
        y,
        "Scan barcode to track shipment",
    )

    c.save()

    return file_path