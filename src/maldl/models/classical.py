"""Training-free handcrafted texture features (baseline against learned encoders).

Per image (standardised to zero mean / unit std, so contrast and brightness do not matter):
  - intensity histogram (16 bins),
  - at 3 Gaussian scales: gradient-magnitude mean/std/histogram (8 bins) and a
    magnitude-weighted gradient-orientation histogram (8 bins),
  - local-binary-pattern style histogram: number of 8-neighbours brighter than the centre (9 bins).
All pure numpy, deterministic, no downloads.
"""
import numpy as np


def _gauss(img, sigma):
    r = max(1, int(3 * sigma))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    p = np.pad(img, r, mode="reflect")
    p = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 0, p)
    return np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, p)


def _hist(v, bins, rng, weights=None):
    h, _ = np.histogram(v, bins=bins, range=rng, weights=weights)
    return h / max(h.sum(), 1e-9)


def image_features(img, sigmas=(1.0, 2.0, 4.0)):
    im = (img - img.mean()) / (img.std() + 1e-6)
    feats = [_hist(im, 16, (-3, 3))]
    for s in sigmas:
        g = _gauss(im, s)
        gy, gx = np.gradient(g)
        mag = np.hypot(gx, gy)
        ang = np.arctan2(gy, gx) % np.pi  # orientation, sign-free
        feats += [np.array([mag.mean(), mag.std()]),
                  _hist(mag, 8, (0, max(mag.max(), 1e-6))),
                  _hist(ang, 8, (0, np.pi), weights=mag)]
    c = im[1:-1, 1:-1]
    brighter = sum((im[1 + dy:im.shape[0] - 1 + dy, 1 + dx:im.shape[1] - 1 + dx] > c).astype(int)
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0))
    feats.append(_hist(brighter, 9, (0, 9)))
    return np.concatenate(feats).astype(np.float32)


def classical_embed(images):
    """images: (N,1,H,W) float array -> (N,D) float32 features."""
    return np.stack([image_features(im[0]) for im in images])
