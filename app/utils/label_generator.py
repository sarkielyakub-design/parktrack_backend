from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_label(shipment, qr_path, barcode_path):

    filename = f"{shipment.tracking_id}.pdf"
    path = f"labels/{filename}"

    c = canvas.Canvas(path, pagesize=letter)

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

    # TRACKING BIG
    c.setFont("Helvetica-Bold", 22)

    c.drawString(
        50,
        680,
        shipment.tracking_id
    )

    # INFO

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
        f"Receiver: {shipment.receiver_name}"
    )

    c.drawString(
        50,
        590,
        f"Phone: {shipment.receiver_phone}"
    )

    c.drawString(
        50,
        570,
        f"Sender: {shipment.sender_name}"
    )

    # BARCODE

    c.drawImage(
        barcode_path,
        50,
        480,
        width=300,
        height=80
    )

    # QR

    c.drawImage(
        qr_path,
        400,
        480,
        width=120,
        height=120
    )

    c.save()

    return f"/labels/{filename}"