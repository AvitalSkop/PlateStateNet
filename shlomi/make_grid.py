#!/usr/bin/env python
"""Build a quick contact-sheet of the generated images for visual QA.

Lays out up to N images per class, one class per row, and saves a single PNG
(shlomi/sample_grid.png) you can open in VSCode and screenshot. Pure CPU, fast.

    python shlomi/make_grid.py            # 10 per class
    python shlomi/make_grid.py --n 6      # 6 per class
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import utils  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=10, help="images per class (columns)")
ap.add_argument("--sz", type=int, default=200, help="thumbnail size in px")
ap.add_argument("--base", default=None,
                help="folder holding per-class subdirs (default: the FLUX synthetic_clean). "
                     "e.g. data/synthetic_clean_gemini for the Gemini A/B set")
ap.add_argument("--out", default=None, help="output PNG path")
args = ap.parse_args()

base = Path(args.base) if args.base else utils.CLEAN_DIR
classes = utils.CLASS_NAMES
grid = Image.new("RGB", (args.n * args.sz, len(classes) * args.sz), "white")
draw = ImageDraw.Draw(grid)

counts = {}
for r, cls in enumerate(classes):
    files = sorted((base / cls).glob("*.jpg"))
    counts[cls] = len(files)
    for j, f in enumerate(files[: args.n]):
        thumb = Image.open(f).convert("RGB").resize((args.sz, args.sz))
        grid.paste(thumb, (j * args.sz, r * args.sz))
    draw.text((4, r * args.sz + 4), cls, fill="red")

default_name = f"sample_grid_{base.name}.png"
out = Path(args.out) if args.out else Path(__file__).resolve().parent / default_name
grid.save(out)
print("saved", out)
print("counts per class:", counts)
