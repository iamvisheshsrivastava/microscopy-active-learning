from itertools import pairwise

import numpy as np


def ece(probs, y, bins=10):
    """Expected calibration error of the top-label confidence."""
    conf = probs.max(1)
    correct = (probs.argmax(1) == y).astype(float)
    edges = np.linspace(0, 1, bins + 1)
    total = 0.0
    for lo, hi in pairwise(edges):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            total += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(total)


def interval_coverage(y, mean, std, z=1.645):
    """Fraction of targets inside mean ± z*std (nominal 0.90 for z=1.645)."""
    return float((np.abs(y - mean) <= z * std).mean())
