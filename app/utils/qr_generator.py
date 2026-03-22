import qrcode
import os


def generate_qr(data, tracking):

    os.makedirs("qr_codes", exist_ok=True)

    path = f"qr_codes/{tracking}.png"

    img = qrcode.make(data)

    img.save(path)

    return path