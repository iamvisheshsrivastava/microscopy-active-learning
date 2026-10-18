"""Loaders for real grayscale micrographs (not bundled, untested on real data).

1. `load_folder(root)`: root/<class_name>/*.png|jpg|tif.
2. `load_table(csv_path, root)`: a metadata CSV with columns
   `path,label` and optional `group` (specimen/sample id), `source` (instrument/lab),
   `magnification`, `property`. Use `group` with `data.splits.group_split`.

Intended for e.g. UHCSDB (NIST, CC BY-SA 3.0; download it yourself, nothing is fetched here).
"""
import csv
from pathlib import Path

import numpy as np
from PIL import Image

EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def _read(path, size):
    im = Image.open(path).convert("L").resize((size, size), Image.BILINEAR)
    return np.asarray(im, dtype=np.float32) / 255.0


def load_folder(root, size=64):
    root = Path(root)
    classes = sorted(p.name for p in root.iterdir() if p.is_dir())
    if not classes:
        raise FileNotFoundError(f"no class sub-folders in {root}")
    xs, ys = [], []
    for ci, c in enumerate(classes):
        for f in sorted((root / c).iterdir()):
            if f.suffix.lower() in EXTS:
                xs.append(_read(f, size))
                ys.append(ci)
    if not xs:
        raise FileNotFoundError(f"no images found under {root}")
    return np.stack(xs)[:, None], np.array(ys, dtype=np.int64), classes


def load_table(csv_path, root=".", size=64):
    """Returns (images (N,1,S,S), labels (N,), classes, meta dict of lists)."""
    root = Path(root)
    with open(csv_path, newline="", encoding="utf-8") as f:
        recs = list(csv.DictReader(f))
    if not recs or not {"path", "label"} <= set(recs[0]):
        raise ValueError("CSV needs at least the columns: path,label")
    classes = sorted({r["label"] for r in recs})
    cid = {c: i for i, c in enumerate(classes)}
    x = np.stack([_read(root / r["path"], size) for r in recs])[:, None]
    y = np.array([cid[r["label"]] for r in recs], dtype=np.int64)
    meta = {k: [r[k] for r in recs] for k in recs[0] if k not in ("path", "label")}
    return x, y, classes, meta
