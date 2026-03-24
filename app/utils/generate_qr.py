import os
import qrcode

BASE_DIR = os.getcwd()

def generate_qr(data, tracking):

    folder = os.path.join(BASE_DIR, "qr_codes")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"{tracking}.png")

    img = qrcode.make(data)
    img.save(path)

    print("QR SAVED:", path)

    return path