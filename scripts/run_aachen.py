"""Active learning on a second real source: Aachen-Heerlen steel SEM (bainitic steels, CC0).

Embeddings come from `scripts/prepare_aachen.py` (frozen DINOv2, built on a GPU). Two tasks, both with
sample-type-grouped splits (10 steel sample types; held-out types are never seen):
  cls  isothermal-transformation temperature (400 vs 500 C) from the image
  reg  martensite-austenite (MA) island area fraction from the expert polygons (GP surrogate)
Real acquisition shifts from the metadata (pool = perpendicular view, vertical cut):
  in_dist          same condition, held-out sample types
  tilt_shift       tilted view
  direction_shift  horizontal cut direction
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.active.loop import run_loop, run_regression_loop  # noqa: E402
from maldl.data.splits import group_split  # noqa: E402
from maldl.eval.stats import curves, markdown_summary  # noqa: E402

SETS = ["in_dist", "tilt_shift", "direction_shift"]
STRATS = ["random", "uncertainty", "diversity", "hybrid"]


def load(emb_dir, backbone):
    with open(Path(emb_dir) / "aachen_targets.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    z = np.load(Path(emb_dir) / f"aachen_emb_{backbone}.npz")
    assert [r["image_url"] for r in rows] == z["image_url"].tolist(), "embedding/target order mismatch"
    meta = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    meta["temperature"] = meta["temperature"].astype(int)
    meta["annotated"] = meta["annotated"].astype(int)
    meta["ma_frac"] = meta["ma_frac"].astype(float)
    return z["emb"].astype(np.float32), meta


def make_split(meta, mask, seed, test_frac, min_eval, need_both_classes):
    types = meta["sample_type"]
    vidx = np.flatnonzero(mask)
    for attempt in range(300):
        tr, te = group_split(types[vidx], test_frac, seed=seed * 1000 + attempt)
        trm, tem = np.zeros(len(types), bool), np.zeros(len(types), bool)
        trm[vidx[tr]], tem[vidx[te]] = True, True
        perp, tilt = meta["angle"] == "perpendicular", meta["angle"] == "tilt"
        vert, horz = meta["direction"] == "Vertical", meta["direction"] == "Horizontal"
        pool = np.flatnonzero(trm & perp & vert)
        ev = {"in_dist": np.flatnonzero(tem & perp & vert), "tilt_shift": np.flatnonzero(tem & tilt & vert),
              "direction_shift": np.flatnonzero(tem & perp & horz)}
        ok = len(pool) >= 100 and all(len(v) >= min_eval for v in ev.values())
        if ok and need_both_classes:
            ok = all(len(np.unique(meta["temperature"][v])) == 2 for v in ev.values()) and \
                len(np.unique(meta["temperature"][pool])) == 2
        if ok:
            assert not set(types[pool]) & set(types[np.concatenate(list(ev.values()))])
            return pool, ev
    raise RuntimeError(f"no valid split for seed {seed}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emb-dir", default="data/cache/aachen")
    ap.add_argument("--backbone", choices=["small", "base"], default="base")
    ap.add_argument("--task", choices=["cls", "reg"], required=True)
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--init", type=int, default=10)
    ap.add_argument("--batch", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--test-frac", type=float, default=0.3)
    ap.add_argument("--min-eval", type=int, default=40)
    ap.add_argument("--out", default="results")
    a = ap.parse_args(argv)
    emb, meta = load(a.emb_dir, a.backbone)
    reg = a.task == "reg"
    mask = meta["annotated"] == 1 if reg else np.ones(len(emb), bool)
    y_cls = (meta["temperature"] == 500).astype(np.int64)
    rows, sizes, baseline = [], [], []
    for seed in range(a.seeds):
        pool, ev = make_split(meta, mask, seed, a.test_frac, a.min_eval, not reg)
        evals = {k: (emb[i], y_cls[i], meta["ma_frac"][i]) for k, i in ev.items()}
        sizes.append({k: len(i) for k, i in ev.items()} | {"pool": len(pool)})
        if reg:
            mu = meta["ma_frac"][pool].mean()
            baseline.append({k: float(np.sqrt(((meta["ma_frac"][i] - mu) ** 2).mean())) for k, i in ev.items()})
        else:
            maj = np.bincount(y_cls[pool], minlength=2).argmax()
            baseline.append({k: float((y_cls[i] == maj).mean()) for k, i in ev.items()})
        for s in STRATS:
            if reg:
                r_ = run_regression_loop(emb[pool], meta["ma_frac"][pool], evals, s, a.init,
                                         a.batch, a.rounds, seed)
            else:
                r_ = run_loop(emb[pool], y_cls[pool], evals, s, a.init, a.batch, a.rounds, seed,
                              num_classes=2)
            rows += [{"strategy": s, "seed": seed, **r} for r in r_]
    name = f"results_aachen_{a.task}_{a.backbone}"
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    metric = (lambda s: f"{s}_rmse") if reg else (lambda s: s)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, st in zip(axes, SETS):
        for s in STRATS:
            c = curves(rows, s, metric(st))
            nl = curves(rows, s, "n_labeled").mean(0)
            ax.plot(nl, c.mean(0), marker="o", label=s)
            ax.fill_between(nl, c.mean(0) - c.std(0), c.mean(0) + c.std(0), alpha=0.1)
        ax.axhline(np.mean([b[st] for b in baseline]), ls=":", c="gray",
                   label="mean predictor" if reg else "majority class")
        ax.set_title(f"Aachen-Heerlen {a.task} / {st}")
        ax.set_xlabel("labels")
        ax.set_ylabel("RMSE of MA area fraction" if reg else "accuracy")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=110)

    msz = {k: float(np.mean([s[k] for s in sizes])) for k in sizes[0]}
    head = (f"DINOv2-{a.backbone}; task={a.task}; grouped by steel sample type; mean sizes: "
            + ", ".join(f"{k}={v:.0f}" for k, v in msz.items()) + "\n"
            + ("Baseline RMSE (predict pool mean): " if reg else "Majority-class accuracy: ")
            + ", ".join(f"{k}={np.mean([b[k] for b in baseline]):.3f}" for k in SETS) + "\n")
    if reg:
        body = ["## RMSE of MA area fraction (lower is better)\n",
                markdown_summary(rows, STRATS, [f"{s}_rmse" for s in SETS], fmt="{:.4f}"),
                "\n## R2 (higher is better)\n",
                markdown_summary(rows, STRATS, [f"{s}_r2" for s in SETS]),
                "\n## 90% interval coverage (nominal 0.90)\n",
                markdown_summary(rows, STRATS, [f"{s}_cov90" for s in SETS])]
    else:
        body = ["## Accuracy\n", markdown_summary(rows, STRATS, SETS),
                "\n## Balanced accuracy\n", markdown_summary(rows, STRATS, [f"{s}_bacc" for s in SETS]),
                "\n## Expected calibration error (lower is better)\n",
                markdown_summary(rows, STRATS, [f"{s}_ece" for s in SETS])]
    (out / f"{name}_summary.md").write_text(head + "\n" + "\n".join(body), encoding="utf-8")
    print(head)
    print("\n".join(body[:2]))


if __name__ == "__main__":
    main()
