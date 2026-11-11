"""Query strategies. All return `b` unique indices drawn from `unlabeled`.

Signature: strategy(emb, unc, labeled, unlabeled, b, rng, cost=None) -> np.ndarray
  emb: (N,D) pool embeddings; unc: (N,) per-item uncertainty (entropy for classification,
  predictive std for regression); cost: (N,) per-item acquisition cost (default 1).
"""
import numpy as np


def entropy(probs):
    p = np.clip(probs, 1e-12, 1.0)
    return -(p * np.log(p)).sum(1)


def least_confidence(probs):
    """1 - max p: larger means the model's top class is less certain."""
    return 1.0 - np.asarray(probs).max(1)


def margin(probs):
    """1 - (p1 - p2) over the top two classes: larger means a closer call."""
    p = np.sort(np.asarray(probs), axis=1)
    if p.shape[1] < 2:
        return np.zeros(len(p))
    return 1.0 - (p[:, -1] - p[:, -2])


UNCERTAINTY_MEASURES = {
    "entropy": entropy,
    "least_confidence": least_confidence,
    "margin": margin,
}


def random_strategy(emb, unc, labeled, unlabeled, b, rng, cost=None):
    return rng.choice(unlabeled, size=min(b, len(unlabeled)), replace=False)


def uncertainty_strategy(emb, unc, labeled, unlabeled, b, rng, cost=None):
    return unlabeled[np.argsort(-unc[unlabeled], kind="stable")[:b]]


def cost_uncertainty_strategy(emb, unc, labeled, unlabeled, b, rng, cost=None):
    """Most uncertainty per unit cost."""
    c = np.ones(len(unc)) if cost is None else np.asarray(cost)
    score = unc[unlabeled] / c[unlabeled]
    return unlabeled[np.argsort(-score, kind="stable")[:b]]


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


def diversity_strategy(emb, unc, labeled, unlabeled, b, rng, cost=None):
    return _kcenter(emb, labeled, unlabeled, b)


def hybrid_strategy(emb, unc, labeled, unlabeled, b, rng, cost=None, pool_mult=4):
    """Top `pool_mult*b` most uncertain candidates, then k-center among them."""
    top = unlabeled[np.argsort(-unc[unlabeled], kind="stable")[: pool_mult * b]]
    return _kcenter(emb, labeled, top, b)


STRATEGIES = {
    "random": random_strategy,
    "uncertainty": uncertainty_strategy,
    "diversity": diversity_strategy,
    "hybrid": hybrid_strategy,
    "cost_uncertainty": cost_uncertainty_strategy,
}
