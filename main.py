#!/usr/bin/env python3
"""World News, 23 November 2026 -- newspaper front page infographic.

The entry image (entry.png, 1024x1024) was drawn for this bounty and ships
in this repository beside this program. This program is the entrypoint the
grader runs: it copies the image to the output directory. It uses only the
Python standard library, as the competition requires: nothing is installed
before it runs, so it cannot depend on Pillow or any other third-party
package at run time.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry image missing: %s" % SOURCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_of(dest) != sha256_of(SOURCE):
        raise SystemExit("copy mismatch: %s differs from %s" % (dest, SOURCE))
    print("wrote %s (%d bytes, sha256 %s)"
          % (dest, os.path.getsize(dest), sha256_of(dest)))


if __name__ == "__main__":
    main()
