import qrcode
import os

QR_FOLDER = "qr_codes"

os.makedirs(QR_FOLDER, exist_ok=True)


def generate_qr(data: str, filename: str):
    path = f"{QR_FOLDER}/{filename}.png"

    img = qrcode.make(data)
    img.save(path)

    return path