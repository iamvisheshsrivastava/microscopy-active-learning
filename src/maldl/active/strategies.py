"""Query strategies. All return `b` unique indices drawn from `unlabeled`.

Signature: strategy(emb, probs, labeled, unlabeled, b, rng) -> np.ndarray of pool indices.
"""
import numpy as np


def random_strategy(emb, probs, labeled, unlabeled, b, rng):
    return rng.choice(unlabeled, size=min(b, len(unlabeled)), replace=False)


def entropy(probs):
    p = np.clip(probs, 1e-12, 1.0)
    return -(p * np.log(p)).sum(1)


def uncertainty_strategy(emb, probs, labeled, unlabeled, b, rng):
    h = entropy(probs[unlabeled])
    return unlabeled[np.argsort(-h, kind="stable")[:b]]


def _kcenter(emb, labeled, candidates, b):
    """Greedy k-center: repeatedly pick the candidate farthest from the chosen set."""
    dmin = np.full(len(candidates), np.inf)
    for r in emb[labeled]:
        dmin = np.minimum(dmin, np.linalg.norm(emb[candidates] - r, axis=1))
    picked = []
    for _ in range(min(b, len(candidates))):
        j = int(np.argmax(dmin))
        picked.append(candidates[j])
        dmin = np.minimum(dmin, np.linalg.norm(emb[candidates] - emb[candidates[j]], axis=1))
        dmin[j] = -1.0
    return np.array(picked)


def diversity_strategy(emb, probs, labeled, unlabeled, b, rng):
    return _kcenter(emb, labeled, unlabeled, b)


def hybrid_strategy(emb, probs, labeled, unlabeled, b, rng, pool_mult=4):
    """Top `pool_mult*b` most uncertain candidates, then k-center among them."""
    h = entropy(probs[unlabeled])
    top = unlabeled[np.argsort(-h, kind="stable")[: pool_mult * b]]
    return _kcenter(emb, labeled, top, b)


STRATEGIES = {
    "random": random_strategy,
    "uncertainty": uncertainty_strategy,
    "diversity": diversity_strategy,
    "hybrid": hybrid_strategy,
}
