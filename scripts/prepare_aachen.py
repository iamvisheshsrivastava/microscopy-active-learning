"""Fetch the Aachen-Heerlen annotated steel SEM dataset (figshare, CC0), build per-image targets
from the expert polygons, and embed the images with a frozen pretrained backbone.

Meant to run on a machine with a fast connection and a GPU (see scripts/kaggle_submit.py --job aachen*):
the image archive is ~1.2 GB. Outputs are small: a targets CSV and embedding .npz files.

Dataset: Iren et al., Scientific Data 2021, doi:10.1038/s41597-021-00926-7; figshare collection
doi:10.6084/m9.figshare.c.5185004.v1 (CC0). Images are never committed to the repo.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

ARTICLES = {"png": 13135625, "metadata": 13135622, "polygons": 13135610}
PT = re.compile(r"\((\d+),\s*(\d+)\)")


def figshare_file(article):
    req = urllib.request.Request(f"https://api.figshare.com/v2/articles/{article}",
                                 headers={"User-Agent": "maldl-dataset-fetch/1.0 (research use; github.com/iamvisheshsrivastava/microscopy-active-learning)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["files"][0]


def download(article, dest_dir, verify=True):
    f = figshare_file(article)
    dest = Path(dest_dir) / f["name"]
    if not dest.exists() or dest.stat().st_size != f["size"]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(f["download_url"], headers={"User-Agent": "maldl-dataset-fetch/1.0 (research use; github.com/iamvisheshsrivastava/microscopy-active-learning)"})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as out:
                    while chunk := r.read(1 << 20):
                        out.write(chunk)
                break
            except urllib.error.HTTPError as e:
                print(f"download {f['name']} failed ({e.code}), retry {attempt + 1}", flush=True)
                time.sleep(20 * (attempt + 1))
        else:
            raise RuntimeError(f"could not download {f['name']}")
    if verify and f.get("computed_md5"):
        h = hashlib.md5()
        with open(dest, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        if h.hexdigest() != f["computed_md5"]:
            raise RuntimeError(f"md5 mismatch for {f['name']}")
        print(f"md5 ok: {f['name']} ({f['size'] / 1e6:.0f} MB)", flush=True)
    return dest


def shoelace(pts):
    x, y = pts[:, 0].astype(float), pts[:, 1].astype(float)
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def load_polygons(path):
    """image -> list of polygon areas in pixels^2 (rows are `image;point;[(x, y), ...]`)."""
    areas = {}
    with open(path, encoding="utf-8-sig") as f:
        next(f)
        for line in f:
            img, _, poly = line.rstrip("\n").split(";", 2)
            pts = np.array(PT.findall(poly), dtype=int)
            if len(pts) >= 3:
                areas.setdefault(img, []).append(shoelace(pts))
    return areas


def load_metadata(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {r["image_url"]: r for r in csv.DictReader(f)}


def read_image(zf, member, crop_bottom, size):
    im = Image.open(io.BytesIO(zf.read(member))).convert("L")
    w, h = im.size
    h2 = h - crop_bottom
    s = min(w, h2)
    left = (w - s) // 2
    im = im.crop((left, 0, left + s, s)).resize((size, size), Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0, (w, h)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/tmp/aachen")
    ap.add_argument("--out", default="results/aachen")
    ap.add_argument("--probe", action="store_true", help="print archive layout/image sizes and save 2 samples")
    ap.add_argument("--crop-bottom", type=int, default=0, help="rows of SEM info banner to drop")
    ap.add_argument("--size", type=int, default=224)
    ap.add_argument("--backbones", nargs="+", default=["facebook/dinov2-small", "facebook/dinov2-base"])
    ap.add_argument("--device", default="cuda")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    meta_p = download(ARTICLES["metadata"], a.work, verify=False)
    poly_p = download(ARTICLES["polygons"], a.work, verify=False)
    zip_p = download(ARTICLES["png"], a.work)
    meta, areas = load_metadata(meta_p), load_polygons(poly_p)
    zf = zipfile.ZipFile(zip_p)
    members = {Path(n).name: n for n in zf.namelist() if n.lower().endswith(".png")}
    print(f"archive: {len(members)} png; metadata rows {len(meta)}; images with polygons {len(areas)}")
    print("example members:", list(members.values())[:3])
    names = sorted(n for n in members if n in meta)
    print(f"in archive and metadata: {len(names)}; of those annotated: {sum(n in areas for n in names)}")
    if a.probe:
        sizes = Counter()
        for n in names[:60]:
            sizes[Image.open(io.BytesIO(zf.read(members[n]))).size] += 1
        print("image sizes:", sizes.most_common(5))
        for n in (names[0], names[len(names) // 2]):
            (out / n).write_bytes(zf.read(members[n]))
        print("saved samples to", out)
        return 0

    imgs, rows = [], []
    for n in names:
        x, (w, h) = read_image(zf, members[n], a.crop_bottom, a.size)
        imgs.append(x)
        ar = areas.get(n, [])
        m = meta[n]
        rows.append({"image_url": n, "sample_type": m["type"], "temperature": m["temperature"],
                     "direction": m["direction"], "angle": m["angle"], "distance": m["distance"],
                     "annotated": int(n in areas), "n_islands": len(ar),
                     "ma_frac": sum(ar) / float(w * (h - a.crop_bottom))})
    with open(out / "aachen_targets.csv", "w", newline="") as f:
        w_ = csv.DictWriter(f, fieldnames=list(rows[0]))
        w_.writeheader()
        w_.writerows(rows)
    x = np.stack(imgs)[:, None]
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from maldl.models.backbone import PretrainedBackbone
    for bb in a.backbones:
        emb = PretrainedBackbone(bb, a.device, a.size)(x)
        tag = bb.split("/")[-1].replace("dinov2-", "")
        np.savez_compressed(out / f"aachen_emb_{tag}.npz", emb=emb.astype(np.float16),
                            image_url=np.array(names))
        print(f"saved embeddings {tag}: {emb.shape}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
