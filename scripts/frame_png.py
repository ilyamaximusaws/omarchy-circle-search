#!/usr/bin/env python3
"""Create the PNG display twin of grim's OCR-friendly PPM, atomically."""
from pathlib import Path
import os
import sys
from PIL import Image

source = Path(sys.argv[1])
target = Path(str(source) + ".png")
tmp = Path(str(target) + f".{os.getpid()}.part")
with Image.open(source) as image:
    image.save(tmp, format="PNG", compress_level=1)
os.replace(tmp, target)
