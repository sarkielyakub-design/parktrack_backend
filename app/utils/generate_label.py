import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = os.getcwd()


def generate_label(
    shipment,
    qr_path,
    barcode_path,
):

    folder = os.path.join(BASE_DIR, "labels")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(
        folder,
        f"{shipment.tracking_id}.pdf"
    )

    c = canvas.Canvas(path, pagesize=A4)

    width, height = A4

    # ================= HEADER =================

    c.setFont("Helvetica-Bold", 26)

    c.drawString(
        40,
        height - 40,
        "ZTECHTRACKIA EXPRESS"
    )

    # line
    c.line(
        40,
        height - 50,
        width - 40,
        height - 50
    )

    # ================= TRACKING BIG =================

    c.setFont("Helvetica-Bold", 32)

    c.drawString(
        40,
        height - 100,
        shipment.tracking_id
    )

    # ================= LEFT INFO =================

    c.setFont("Helvetica", 14)

    y = height - 150

    c.drawString(40, y, f"Sender: {shipment.sender_name}")
    y -= 20

    c.drawString(40, y, f"Phone: {shipment.sender_phone}")
    y -= 20

    c.drawString(40, y, f"Receiver: {shipment.receiver_name}")
    y -= 20

    c.drawString(40, y, f"Phone: {shipment.receiver_phone}")
    y -= 20

    c.drawString(40, y, f"From: {shipment.from_city}")
    y -= 20

    c.drawString(40, y, f"To: {shipment.to_city}")
    y -= 20

    c.drawString(40, y, f"Price: {shipment.price}")
    y -= 20

    c.drawString(40, y, f"Note: {shipment.note}")

    # ================= QR RIGHT =================

    if os.path.exists(qr_path):

        c.drawImage(
            qr_path,
            width - 200,
            height - 250,
            150,
            150
        )

    # ================= BIG BARCODE =================

    if os.path.exists(barcode_path):

        c.drawImage(
            barcode_path,
            40,
            300,
            width - 80,
            120
        )

    # ================= TRACKING AGAIN =================

    c.setFont("Helvetica-Bold", 24)

    c.drawCentredString(
        width / 2,
        260,
        shipment.tracking_id
    )

    # ================= FOOTER =================

    c.setFont("Helvetica", 12)

    c.drawString(
        40,
        200,
        "Powered by ZTECHTRACKIA Logistics System"
    )

    c.save()

    print("LABEL SAVED:", path)

    return path