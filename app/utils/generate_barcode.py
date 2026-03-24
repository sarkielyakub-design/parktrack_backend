import os
import barcode
from barcode.writer import ImageWriter
from app.config import BARCODE_DIR


def generate_barcode(tracking):

    path = os.path.join(
        BARCODE_DIR,
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