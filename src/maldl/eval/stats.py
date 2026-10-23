"""Learning-curve summaries and paired significance tests across seeds."""
import warnings

import numpy as np
from scipy.stats import wilcoxon


def curves(rows, strategy, metric):
    """-> (seeds, rounds) matrix of `metric` for one strategy."""
    seeds = sorted({r["seed"] for r in rows if r["strategy"] == strategy})
    rounds = sorted({r["round"] for r in rows if r["strategy"] == strategy})
    d = {(r["seed"], r["round"]): r[metric] for r in rows if r["strategy"] == strategy}
    return np.array([[d[(s, k)] for k in rounds] for s in seeds])


def alc(mat):
    """Area under the learning curve, per seed (mean over rounds)."""
    return mat.mean(1)


def paired_test(a, b):
    """Two-sided Wilcoxon signed-rank on per-seed values; returns (mean diff, p)."""
    d = np.asarray(a) - np.asarray(b)
    if np.allclose(d, 0):
        return 0.0, 1.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return float(d.mean()), float(wilcoxon(a, b).pvalue)


def markdown_summary(rows, strategies, metrics, baseline="random", fmt="{:.3f}"):
    """Final-round value (mean±std) and ALC, plus ALC difference vs `baseline` with p-value."""
    n_seeds = len({r["seed"] for r in rows})
    out = [f"Final round, mean±std over {n_seeds} seeds; ALC (mean over rounds) in parentheses.\n",
           "| strategy | " + " | ".join(metrics) + " |",
           "|---|" + "---|" * len(metrics)]
    for s in strategies:
        cells = []
        for m in metrics:
            c = curves(rows, s, m)
            cells.append(f"{fmt.format(c[:, -1].mean())}±{fmt.format(c[:, -1].std())} "
                         f"({fmt.format(alc(c).mean())})")
        out.append(f"| {s} | " + " | ".join(cells) + " |")
    others = [s for s in strategies if s != baseline]
    res = {(s, m): (*paired_test(alc(curves(rows, s, m)), alc(curves(rows, baseline, m))),
                    bootstrap_ci(alc(curves(rows, s, m)) - alc(curves(rows, baseline, m))))
           for s in others for m in metrics}
    keys = list(res)
    adj = dict(zip(keys, holm([res[k][1] for k in keys])))
    out += ["", f"ALC difference vs `{baseline}`: mean diff [95% bootstrap CI over seeds], "
                f"Wilcoxon p, Holm-adjusted p over all {len(keys)} cells of this table "
                f"(p cannot go below ~{2 / 2 ** n_seeds:.3f} with {n_seeds} seeds).\n",
            "| strategy | " + " | ".join(metrics) + " |", "|---|" + "---|" * len(metrics)]
    for s in others:
        cells = []
        for m in metrics:
            d, p, (lo, hi) = res[(s, m)]
            cells.append(f"{d:+.3f} [{lo:+.3f}, {hi:+.3f}] p={p:.2f} (Holm {adj[(s, m)]:.2f})")
        out.append(f"| {s} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def holm(pvals):
    """Holm-Bonferroni adjusted p-values, in the input order."""
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = running
    return adj.tolist()


def bootstrap_ci(diffs, n_boot=2000, alpha=0.05, seed=0):
    """Percentile bootstrap CI of the mean of per-seed paired differences."""
    d = np.asarray(diffs, dtype=float)
    rng = np.random.default_rng(seed)
    means = rng.choice(d, size=(n_boot, len(d)), replace=True).mean(1)
    return float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))
