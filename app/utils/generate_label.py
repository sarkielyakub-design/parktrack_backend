import os
from reportlab.lib.pagesizes import letter
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

    c = canvas.Canvas(path, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)

    c.drawString(
        50,
        750,
        "ZTECHTRACKIA EXPRESS"
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        720,
        f"Tracking: {shipment.tracking_id}"
    )

    c.drawString(
        50,
        700,
        f"From: {shipment.from_city}"
    )

    c.drawString(
        50,
        680,
        f"To: {shipment.to_city}"
    )

    c.drawString(
        50,
        660,
        f"Receiver: {shipment.receiver_name}"
    )

    if os.path.exists(barcode_path):

        c.drawImage(
            barcode_path,
            50,
            580,
            250,
            80
        )

    if os.path.exists(qr_path):

        c.drawImage(
            qr_path,
            320,
            580,
            120,
            120
        )

    c.save()

    print("LABEL SAVED:", path)

    return path