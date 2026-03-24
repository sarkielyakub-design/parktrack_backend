import os
import barcode
from barcode.writer import ImageWriter

BASE_DIR = os.getcwd()


def generate_barcode(tracking):

    folder = os.path.join(BASE_DIR, "barcodes")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(
        folder,
        tracking
    )

    code = barcode.get(
        "code128",
        tracking,
        writer=ImageWriter()
    )

    full = code.save(path)

    print("BARCODE SAVED:", full)

    return full