"""Pool-based active learning on frozen embeddings.

Classification: logistic-regression head, uncertainty = predictive entropy.
Regression: GP surrogate on the embeddings, uncertainty = predictive std.
Eval sets: {name: (emb, y_class, y_property)}; classification only needs the first two,
regression needs the third.
"""
import warnings

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, r2_score
from sklearn.preprocessing import StandardScaler

from ..eval.calibration import ece, interval_coverage
from ..models.surrogate import GPSurrogate
from .strategies import STRATEGIES, entropy


def _fit(emb, y, labeled):
    sc = StandardScaler().fit(emb[labeled])
    clf = LogisticRegression(max_iter=500, C=1.0).fit(sc.transform(emb[labeled]), y[labeled])
    return sc, clf


def _proba(sc, clf, emb, num_classes):
    full = np.zeros((len(emb), num_classes))
    full[:, clf.classes_] = clf.predict_proba(sc.transform(emb))
    return full


def _select(strat, emb, unc, labeled, n, b, rng, cost):
    mask = np.ones(n, bool)
    mask[labeled] = False
    unlabeled = np.flatnonzero(mask)
    pick = np.asarray(strat(emb, unc, labeled, unlabeled, b, rng, cost=cost))
    if len(set(pick.tolist())) != len(pick) or set(pick.tolist()) & set(labeled.tolist()):
        raise RuntimeError("strategy returned duplicate or already-labeled indices")
    return np.concatenate([labeled, pick])


def run_loop(pool_emb, pool_y, eval_sets, strategy, init=8, batch=8, rounds=8,
             seed=0, num_classes=4, costs=None):
    """Classification loop. Returns one dict row per round (incl. round 0)."""
    rng = np.random.default_rng(seed)
    n = len(pool_y)
    costs = np.ones(n) if costs is None else np.asarray(costs, dtype=float)
    labeled = rng.choice(n, size=init, replace=False)
    strat = STRATEGIES[strategy]
    rows = []
    for r in range(rounds + 1):
        sc, clf = _fit(pool_emb, pool_y, labeled)
        row = {"round": r, "n_labeled": len(labeled), "cum_cost": float(costs[labeled].sum())}
        for name, v in eval_sets.items():
            e, y = v[0], v[1]
            p = _proba(sc, clf, e, num_classes)
            row[name] = float((p.argmax(1) == y).mean())
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                row[f"{name}_bacc"] = float(balanced_accuracy_score(y, p.argmax(1)))
            row[f"{name}_ece"] = ece(p, y)
            row[f"{name}_conf"] = float(p.max(1).mean())
        rows.append(row)
        if r == rounds:
            break
        unc = entropy(_proba(sc, clf, pool_emb, num_classes))
        labeled = _select(strat, pool_emb, unc, labeled, n, batch, rng, costs)
    return rows


def run_regression_loop(pool_emb, pool_prop, eval_sets, strategy, init=8, batch=8,
                        rounds=8, seed=0, costs=None):
    """Regression loop with a GP surrogate. Rows hold R2, RMSE and 90%-interval coverage."""
    rng = np.random.default_rng(seed)
    n = len(pool_prop)
    costs = np.ones(n) if costs is None else np.asarray(costs, dtype=float)
    gp = GPSurrogate(pool_emb)
    labeled = rng.choice(n, size=init, replace=False)
    strat = STRATEGIES[strategy]
    rows = []
    for r in range(rounds + 1):
        gp.fit(pool_emb[labeled], pool_prop[labeled])
        row = {"round": r, "n_labeled": len(labeled), "cum_cost": float(costs[labeled].sum())}
        for name, v in eval_sets.items():
            e, yp = v[0], v[2]
            mean, std = gp.predict(e)
            row[f"{name}_r2"] = float(r2_score(yp, mean))
            row[f"{name}_rmse"] = float(np.sqrt(((yp - mean) ** 2).mean()))
            row[f"{name}_cov90"] = interval_coverage(yp, mean, std)
        rows.append(row)
        if r == rounds:
            break
        _, unc = gp.predict(pool_emb)
        labeled = _select(strat, pool_emb, unc, labeled, n, batch, rng, costs)
    return rows
