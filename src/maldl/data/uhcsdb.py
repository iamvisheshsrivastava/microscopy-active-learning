"""Loader for the UHCSDB ultrahigh-carbon-steel SEM micrographs (DeCost et al. 2017, CC BY 3.0 US).

Works with the Zenodo-archived GitHub mirror (https://github.com/rydia001/UHCS_micrographs_mirror,
doi:10.5281/zenodo.23050463) because the original NIST host was unreachable. Expects
`root/metadata.csv` (columns incl. path, primary_microconstituent, detector, magnification,
sample_key) and `root/micrographs/`. Data is never bundled; download it yourself.

Preprocessing: crop away the SEM data banner (bottom rows), centre-crop to a square, resize.
"""
import csv
import re
from pathlib import Path

import numpy as np
from PIL import Image

BANNER_ROWS = 38  # 522-px-high UHCSDB images carry a 38-px info bar at the bottom


def _parse_mag(s):
    m = re.search(r"[\d.]+", s or "")
    return float(m.group()) if m else float("nan")


def _read(path, size):
    im = Image.open(path).convert("L")
    w, h = im.size
    h = h - BANNER_ROWS if h > 500 else h
    s = min(w, h)
    left, top = (w - s) // 2, 0
    im = im.crop((left, top, left + s, top + s)).resize((size, size), Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0


def load_uhcsdb(root, size=64, cache_dir=None):
    """Returns (images (N,1,S,S) float32, meta dict of numpy arrays, class_names).

    meta keys: y (int label), label (str), detector, magnification (float), group (specimen id), path.
    Rows without a specimen id get a unique group each (never merged into one fake specimen).
    """
    root = Path(root)
    cache = Path(cache_dir) / f"uhcsdb_{size}.npz" if cache_dir else None
    with open(root / "metadata.csv", newline="", encoding="utf-8") as f:
        recs = list(csv.DictReader(f))
    classes = sorted({r["primary_microconstituent"] for r in recs})
    cid = {c: i for i, c in enumerate(classes)}
    if cache and cache.exists():
        x = np.load(cache)["x"]
    else:
        x = np.stack([_read(root / "micrographs" / r["path"], size) for r in recs])[:, None]
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(cache, x=x)
    meta = {
        "y": np.array([cid[r["primary_microconstituent"]] for r in recs], dtype=np.int64),
        "label": np.array([r["primary_microconstituent"] for r in recs]),
        "detector": np.array([r["detector"] or "unknown" for r in recs]),
        "magnification": np.array([_parse_mag(r["magnification"]) for r in recs]),
        "group": np.array([r["sample_key"] or f"nokey_{r['micrograph_id']}" for r in recs]),
        "path": np.array([r["path"] for r in recs]),
    }
    return x, meta, classes
