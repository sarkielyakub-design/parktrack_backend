import os
import barcode
from barcode.writer import ImageWriter

BASE_DIR = os.getcwd()


def generate_barcode(tracking):

    folder = os.path.join(BASE_DIR, "barcodes")
    os.makedirs(folder, exist_ok=True)

    filename = tracking

    path = os.path.join(folder, filename)

    code = barcode.get(
        "code128",
        tracking,
        writer=ImageWriter()
    )

    full_path = code.save(path)

    return full_path