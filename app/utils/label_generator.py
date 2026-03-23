from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


BASE_DIR = os.getcwd()


def generate_label(shipment, qr_path, barcode_path):

    os.makedirs("labels", exist_ok=True)

    filename = f"{shipment.tracking_id}.pdf"

    file_path = os.path.join(
        BASE_DIR,
        "labels",
        filename
    )

    qr_real = os.path.join(
        BASE_DIR,
        qr_path.lstrip("/")
    )

    barcode_real = os.path.join(
        BASE_DIR,
        barcode_path.lstrip("/")
    )

    c = canvas.Canvas(
        file_path,
        pagesize=letter
    )

    # ================= HEADER =================

    c.setFillColorRGB(1, 0.85, 0)
    c.rect(0, 720, 600, 80, fill=1)

    c.setFont("Helvetica-Bold", 20)

    c.drawString(
        40,
        760,
        "ZTECHTRACKIA EXPRESS"
    )

    # ================= TRACKING =================

    c.setFont("Helvetica-Bold", 26)

    c.drawString(
        40,
        700,
        shipment.tracking_id
    )

    # ================= BOX =================

    c.rect(40, 520, 520, 160)

    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        650,
        f"FROM: {shipment.from_city}"
    )

    c.drawString(
        50,
        630,
        f"TO: {shipment.to_city}"
    )

    c.drawString(
        50,
        610,
        f"SENDER: {shipment.sender_name}"
    )

    c.drawString(
        50,
        590,
        f"RECEIVER: {shipment.receiver_name}"
    )

    c.drawString(
        50,
        570,
        f"PHONE: {shipment.receiver_phone}"
    )

    c.drawString(
        50,
        550,
        f"PRICE: {shipment.price}"
    )

    # ================= BARCODE =================

    if os.path.exists(barcode_real):

        c.drawImage(
            barcode_real,
            60,
            450,
            width=400,
            height=80
        )

    # ================= QR =================

    if os.path.exists(qr_real):

        c.drawImage(
            qr_real,
            470,
            450,
            width=90,
            height=90
        )

    # ================= FOOTER =================

    c.setFont("Helvetica", 10)

    c.drawString(
        40,
        420,
        "Powered by ZTECHTRACKIA Logistics System"
    )

    c.save()

    return f"/labels/{filename}"