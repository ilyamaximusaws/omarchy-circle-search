#!/usr/bin/env python3
"""Build a local, immediately-submitting Google Lens upload page for an image file."""
import base64
from pathlib import Path
import os
import time

PAGE = '''<!doctype html><meta charset="utf-8"><title>Google Lens…</title>
<body style="background:#111;color:#ddd;font:16px sans-serif;display:grid;place-items:center;height:100vh;margin:0">
<form id="f" method="post" enctype="multipart/form-data" action="https://lens.google.com/v3/upload?ep=ccm&amp;st={ts}">
<input type="file" name="encoded_image" id="i" hidden></form><p>Google Lens…</p>
<script>
const b = atob("{data}"), a = new Uint8Array(b.length);
for (let k = 0; k < b.length; k++) a[k] = b.charCodeAt(k);
const dt = new DataTransfer();
dt.items.add(new File([a], "circle-search.png", {{type: "image/png"}}));
document.getElementById("i").files = dt.files;
document.getElementById("f").submit();
</script>'''


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    data = base64.b64encode(args.image.read_bytes()).decode()
    runtime = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"))
    runtime.mkdir(parents=True, exist_ok=True)
    page = runtime / "omarchy-circle-search-lens.html"
    page.write_text(PAGE.format(data=data, ts=int(time.time() * 1000)))
    print(page)


if __name__ == "__main__":
    main()
