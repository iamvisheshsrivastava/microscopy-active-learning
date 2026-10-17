"""Pool-based active learning on frozen embeddings with a logistic-regression head."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from .strategies import STRATEGIES


def _fit(emb, y, labeled):
    sc = StandardScaler().fit(emb[labeled])
    clf = LogisticRegression(max_iter=500, C=1.0).fit(sc.transform(emb[labeled]), y[labeled])
    return sc, clf


def _proba(sc, clf, emb, num_classes):
    full = np.zeros((len(emb), num_classes))
    full[:, clf.classes_] = clf.predict_proba(sc.transform(emb))
    return full


def run_loop(pool_emb, pool_y, eval_sets, strategy, init=8, batch=8, rounds=8,
             seed=0, num_classes=4):
    """eval_sets: {name: (emb, y)}. Returns one dict row per round (incl. round 0)."""
    rng = np.random.default_rng(seed)
    n = len(pool_y)
    labeled = rng.choice(n, size=init, replace=False)
    strat = STRATEGIES[strategy]
    rows = []
    for r in range(rounds + 1):
        sc, clf = _fit(pool_emb, pool_y, labeled)
        row = {"round": r, "n_labeled": len(labeled)}
        for name, (e, y) in eval_sets.items():
            row[name] = float((clf.predict(sc.transform(e)) == y).mean())
        rows.append(row)
        if r == rounds:
            break
        mask = np.ones(n, bool)
        mask[labeled] = False
        unlabeled = np.flatnonzero(mask)
        probs = _proba(sc, clf, pool_emb, num_classes)
        pick = np.asarray(strat(pool_emb, probs, labeled, unlabeled, batch, rng))
        if len(set(pick.tolist())) != len(pick) or set(pick.tolist()) & set(labeled.tolist()):
            raise RuntimeError("strategy returned duplicate or already-labeled indices")
        labeled = np.concatenate([labeled, pick])
    return rows
