import os
import qrcode


def generate_qr(data, tracking):

    folder = "qr_codes"
    os.makedirs(folder, exist_ok=True)

    filename = f"{tracking}.png"

    path = os.path.join(folder, filename)

    img = qrcode.make(data)

    img.save(path)

    return {
        "file": path,
        "url": f"/qr/{filename}"
    }