import os
import qrcode
from app.config import QR_DIR


def generate_qr(data, tracking):

    path = os.path.join(
        QR_DIR,
        f"{tracking}.png"
    )

    img = qrcode.make(data)
    img.save(path)

    print("QR SAVED:", path)

    return path