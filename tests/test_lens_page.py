#!/usr/bin/env python3
import base64
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
script = ROOT / "scripts/lens_page.py"
assert script.exists(), "lens_page.py is missing"
with tempfile.TemporaryDirectory() as tmp:
    image = Path(tmp) / "crop.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\nfake-test-image")
    result = subprocess.run([sys.executable, str(script), str(image)], env={"XDG_RUNTIME_DIR": tmp}, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    page = Path(result.stdout.strip())
    assert page.is_file()
    html = page.read_text()
    assert 'action="https://lens.google.com/v3/upload' in html
    assert 'name="encoded_image"' in html
    assert base64.b64encode(image.read_bytes()).decode() in html
    assert "new File" in html and "submit()" in html
    assert "<img" not in html, "the local upload page must not render the image remotely"
print("PASS local Google Lens upload page")
