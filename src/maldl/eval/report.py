"""Shared CSV-writing and learning-curve plotting for the experiment scripts."""
import csv

import numpy as np

from .stats import curves


def write_rows_csv(rows, path):
    """Write a list of dicts as CSV, with columns in the order of the first row."""
    if not rows:
        raise ValueError("no rows to write")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def plot_learning_curves(rows, metrics, strategies, path, *, metric_columns=None, titles=None,
                         ylabel=None, baseline=None, baseline_label=None, cost_metric=None,
                         cost_title=None, figsize=None, dpi=110):
    """Plot mean±std learning curves per metric, plus an optional cumulative-cost panel.

    `metrics` names the panels and the default curve column; `metric_columns` overrides the
    column read for each panel (e.g. an `_rmse` suffix). `baseline` maps metric -> reference value.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    columns = metric_columns or metrics
    titles = titles or metrics
    n = len(metrics) + (1 if cost_metric else 0)
    fig, axes = plt.subplots(1, n, figsize=figsize or ((19, 4) if n > 3 else (15, 4)))
    axes = np.atleast_1d(axes)
    for ax, m, col, title in zip(axes, metrics, columns, titles):
        for s in strategies:
            c = curves(rows, s, col)
            nl = curves(rows, s, "n_labeled").mean(0)
            ax.plot(nl, c.mean(0), marker="o", label=s)
            ax.fill_between(nl, c.mean(0) - c.std(0), c.mean(0) + c.std(0), alpha=0.1)
        if baseline is not None:
            ax.axhline(baseline[m], ls=":", c="gray", label=baseline_label)
        ax.set_title(title)
        ax.set_xlabel("labels")
        if ylabel:
            ax.set_ylabel(ylabel)
    if cost_metric:
        ax = axes[-1]
        for s in strategies:
            ax.plot(curves(rows, s, cost_metric).mean(0), curves(rows, s, "in_dist").mean(0),
                    marker="o", label=s)
        ax.set_title(cost_title or f"in_dist vs cumulative {cost_metric}")
        ax.set_xlabel("cost units")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=dpi)
    return fig, axes
