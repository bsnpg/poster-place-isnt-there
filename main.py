#!/usr/bin/env python3
"""poster-place-isnt-there: place the entry image where the grader expects it.

The image is entry.png sitting next to this file. The grader runs this
program twice and requires both runs to write identical bytes, so the
program only copies the file — it never redraws, edits, or re-encodes it.
Run it outside the grader with MAKEFUN_OUTPUT_DIR set to a scratch dir:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    image = os.path.join(here, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    with open(image, "rb") as src:
        data = src.read()
    with open(target, "wb") as dst:
        dst.write(data)


if __name__ == "__main__":
    main()
