"""Seeded synthetic microstructure generator (offline, no data files).

Four texture classes, loosely modelled on steel micrographs:
  0 fine equiaxed grains, 1 coarse equiaxed grains,
  2 lamellar (striped) grains, 3 grains with dark precipitates.
`scale` mimics magnification: all pixel feature sizes are multiplied by it.
`Source` mimics a different instrument (contrast, noise, blur, offset).

Each sample also has a paired EBSD-like map (2 channels encoding a per-grain
orientation angle; boundaries and precipitates are "non-indexed" = 0) and a scalar
property computed from the structure (Hall-Petch-like hardness). The property
formula and annotation-cost model are ASSUMPTIONS for testing the pipeline,
not materials science.
"""
from dataclasses import dataclass

import numpy as np

CLASS_NAMES = ["fine", "coarse", "lamellar", "precipitate"]
NUM_CLASSES = len(CLASS_NAMES)


@dataclass(frozen=True)
class Source:
    contrast: float = 1.0
    noise: float = 0.05
    blur: float = 0.8
    offset: float = 0.0


SOURCE_A = Source()
SOURCE_B = Source(contrast=0.6, noise=0.12, blur=1.6, offset=0.15)


def _blur(img, sigma):
    if sigma <= 0:
        return img
    r = max(1, int(3 * sigma))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.pad(img, r, mode="reflect")
    pad = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 0, pad)
    pad = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, pad)
    return pad


def _structure(cls, rng, size, scale):
    """Clean microstructure: grayscale image, grain labels, orientation, property."""
    n_base = {0: 70, 1: 14, 2: 16, 3: 16}[cls]
    n = max(2, int(round(n_base / scale**2 * rng.uniform(0.8, 1.2))))
    seeds = rng.uniform(0, size, (n, 2))
    yy, xx = np.mgrid[0:size, 0:size]
    pts = np.stack([yy, xx], -1).reshape(-1, 1, 2)
    d = ((pts - seeds[None]) ** 2).sum(-1)
    lab = d.argmin(1).reshape(size, size)
    d_sorted = np.sort(d, 1)
    edge = (np.sqrt(d_sorted[:, 1]) - np.sqrt(d_sorted[:, 0])).reshape(size, size) < 1.0
    img = rng.uniform(0.3, 0.7, n)[lab]
    theta = rng.uniform(0, np.pi, n)  # grain orientation (EBSD)
    prec = np.zeros((size, size), bool)
    period = 0.0
    if cls == 2:
        period = 4.0 * rng.uniform(0.9, 1.1)  # physical period, scale-free
        phase = rng.uniform(0, 2 * np.pi, n)
        proj = np.cos(theta)[lab] * xx + np.sin(theta)[lab] * yy
        img = img + 0.22 * np.sin(2 * np.pi * proj / (period * scale) + phase[lab])
    if cls == 3:
        for _ in range(int(rng.integers(40, 70) / scale**2)):
            cy, cx = rng.uniform(0, size, 2)
            r = rng.uniform(1.0, 2.0) * scale
            prec |= (yy - cy) ** 2 + (xx - cx) ** 2 < r**2
        img[prec] = 0.08
    img[edge] = np.minimum(img[edge], 0.12)
    d_phys = size / np.sqrt(n) / scale  # mean grain diameter in scale-1 pixels
    prop = 150.0 + 900.0 / np.sqrt(d_phys)
    if cls == 2:
        prop += 200.0 / period
    if cls == 3:
        prop += 600.0 * prec.mean()
    prop += rng.normal(0, 5.0)
    return dict(img=img, lab=lab, edge=edge, prec=prec, theta=theta, n=n,
                prop=float(prop))


def _sem(s, rng, source):
    img = _blur(s["img"], source.blur)
    img = 0.5 + (img - 0.5) * source.contrast + source.offset
    img = img + rng.normal(0, source.noise, img.shape)
    return np.clip(img, 0, 1).astype(np.float32)


def _ebsd(s, rng):
    th = s["theta"][s["lab"]]
    e = np.stack([0.5 + 0.5 * np.cos(2 * th), 0.5 + 0.5 * np.sin(2 * th)])
    e[:, s["edge"] | s["prec"]] = 0.0  # non-indexed pixels
    e = e + rng.normal(0, 0.02, e.shape)
    return np.clip(e, 0, 1).astype(np.float32)


def _cost(n):
    # ASSUMED annotation-time proxy: more grains in view -> more effort.
    return 1.0 + n / 20.0


def generate_image(cls, rng, size=64, scale=1.0, source=SOURCE_A):
    s = _structure(cls, rng, size, scale)
    return _sem(s, rng, source)


def _info(ss):
    return {"property": np.array([s["prop"] for s in ss], dtype=np.float64),
            "n_grains": np.array([s["n"] for s in ss]),
            "cost": np.array([_cost(s["n"]) for s in ss], dtype=np.float64)}


def _labels(n, rng):
    y = np.arange(n) % NUM_CLASSES
    rng.shuffle(y)
    return y


def make_dataset(n, seed, size=64, scale=1.0, source=SOURCE_A, return_info=False):
    """Balanced dataset; returns (N,1,size,size) float32 images and int labels."""
    rng = np.random.default_rng(seed)
    y = _labels(n, rng)
    ss = [_structure(int(c), rng, size, scale) for c in y]
    x = np.stack([_sem(s, rng, source) for s in ss])[:, None]
    y = y.astype(np.int64)
    return (x, y, _info(ss)) if return_info else (x, y)


def make_paired_dataset(n, seed, size=64, scale=1.0, source=SOURCE_A):
    """Registered SEM + EBSD pairs. Returns sem (N,1,S,S), ebsd (N,2,S,S), y, info.
    `source` only affects the SEM channel (EBSD is a different instrument)."""
    rng = np.random.default_rng(seed)
    y = _labels(n, rng)
    ss = [_structure(int(c), rng, size, scale) for c in y]
    sem = np.stack([_sem(s, rng, source) for s in ss])[:, None]
    ebsd = np.stack([_ebsd(s, rng) for s in ss])
    return sem, ebsd, y.astype(np.int64), _info(ss)
