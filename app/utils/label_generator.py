from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
import os


LABEL_FOLDER = "labels"

LOGO_PATH = "assets/logo.png"

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

    # ---------- LOGO ----------

    if os.path.exists(LOGO_PATH):

        c.drawImage(
            LOGO_PATH,
            10,
            380,
            width=40,
            height=40,
        )

    # ---------- HEADER ----------

    c.setFont("Helvetica-Bold", 14)

    c.drawString(
        60,
        400,
        "ZTECHTRACKIA"
    )

    c.setFont("Helvetica", 9)

    c.drawString(
        60,
        385,
        "Courier Delivery Label"
    )

    # ---------- TRACKING ----------

    c.setFont("Helvetica-Bold", 12)

    c.drawString(
        10,
        360,
        f"Tracking: {shipment.tracking_id}"
    )

    # ---------- SENDER ----------

    c.setFont("Helvetica", 9)

    c.drawString(
        10,
        340,
        f"Sender: {shipment.sender_name}"
    )

    c.drawString(
        10,
        325,
        f"Phone: {shipment.sender_phone}"
    )

    # ---------- RECEIVER ----------

    c.drawString(
        10,
        305,
        f"Receiver: {shipment.receiver_name}"
    )

    c.drawString(
        10,
        290,
        f"Phone: {shipment.receiver_phone}"
    )

    # ---------- ROUTE ----------

    c.drawString(
        10,
        270,
        f"From: {shipment.from_city}"
    )

    c.drawString(
        10,
        255,
        f"To: {shipment.to_city}"
    )

    # ---------- QR ----------

    if qr_path:

        c.drawImage(
            qr_path,
            170,
            300,
            width=100,
            height=100,
        )

    # ---------- BARCODE ----------

    if barcode_path:

        c.drawImage(
            barcode_path,
            20,
            200,
            width=240,
            height=60,
        )

    # ---------- FOOTER ----------

    c.setFont("Helvetica", 8)

    c.drawString(
        10,
        180,
        "Handle with care"
    )

    c.drawString(
        10,
        165,
        "ZtechTrackia Delivery System"
    )

    c.save()

    return file_path