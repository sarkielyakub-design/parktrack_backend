import qrcode
import os


def generate_qr(data, tracking):

    os.makedirs("qr_codes", exist_ok=True)

    filename = f"{tracking}.png"

    file_path = f"qr_codes/{filename}"

    img = qrcode.make(data)

    img.save(file_path)

    # ✅ return API URL path
    return f"/qr/{filename}"