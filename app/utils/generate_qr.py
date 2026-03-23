import os
import qrcode

BASE_DIR = os.getcwd()


def generate_qr(data, tracking):

    folder = os.path.join(BASE_DIR, "qr_codes")
    os.makedirs(folder, exist_ok=True)

    filename = f"{tracking}.png"

    path = os.path.join(folder, filename)

    img = qrcode.make(data)
    img.save(path)

    return path