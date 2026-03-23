import os
import barcode
from barcode.writer import ImageWriter


def generate_barcode(tracking):

    folder = "barcodes"
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