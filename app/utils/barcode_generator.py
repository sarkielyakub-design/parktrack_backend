import barcode
from barcode.writer import ImageWriter
import os


def generate_barcode(tracking):

    os.makedirs("barcodes", exist_ok=True)

    path = f"barcodes/{tracking}"

    code = barcode.get(
        "code128",
        tracking,
        writer=ImageWriter(),
    )

    filename = code.save(path)

    return f"barcodes/{tracking}.png"