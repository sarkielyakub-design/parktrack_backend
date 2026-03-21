import barcode
from barcode.writer import ImageWriter
import os

BAR_FOLDER = "barcodes"

os.makedirs(BAR_FOLDER, exist_ok=True)


def generate_barcode(code):

    path = f"{BAR_FOLDER}/{code}"

    barcode_class = barcode.get_barcode_class("code128")

    my_barcode = barcode_class(
        code,
        writer=ImageWriter()
    )

    filename = my_barcode.save(path)

    return filename