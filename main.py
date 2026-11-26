"""Program entri news-image-20261125.

Menyalin poster.png yang sudah dirender di repo ini ke /output/entry.png.
Tidak ada network, hanya stdlib. Salinan byte-per-byte, jadi dua kali jalan
selalu menghasilkan file yang identik.
"""

import hashlib
import os
import shutil

POSTER_NAME = "poster.png"
OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"


def poster_path():
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, POSTER_NAME)


def main():
    source = poster_path()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    shutil.copyfile(source, target)
    with open(target, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote " + target + " sha256=" + digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
