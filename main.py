#!/usr/bin/env python3
"""Entry program for the 25 November 2026 front page.

Standard library only. Copies the bundled entry.png (1024x1024, under
1 MiB) to MAKEFUN_OUTPUT_DIR/entry.png, verifying the PNG header, the
declared dimensions and the byte count before and after the copy.
No network, no rendering, no writes outside the output directory.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_bundled():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as handle:
        return handle.read()


def check_png(data):
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too large: {len(data)} bytes")
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"unexpected dimensions: {width}x{height}")
    if not (len(data) >= 12 and data[-12:-8] == b"\x00\x00\x00\x00"
            and data[-8:-4] == b"IEND"):
        raise SystemExit("entry.png is truncated: missing IEND chunk")
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    data = read_bundled()
    check_png(data)
    target = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)
    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("written entry.png does not match the bundle")
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {len(written)} bytes to {target} sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
