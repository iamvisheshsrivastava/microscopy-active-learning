"""Seeded classification experiment: query strategies on frozen embeddings.

Variants: default = baseline (weak augmentation, no input normalisation).
`--norm-input --strong-aug` = instrument-robustness variant.
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.active.loop import run_loop  # noqa: E402
from maldl.active.strategies import STRATEGIES  # noqa: E402
from maldl.data.synthetic import make_dataset  # noqa: E402
from maldl.eval.shift import build_eval_sets  # noqa: E402
from maldl.eval.stats import curves, markdown_summary  # noqa: E402
from maldl.models.encoder import Encoder  # noqa: E402
from maldl.training.contrastive import embed, pretrain  # noqa: E402

METRICS = ["in_dist", "scale_shift", "source_shift"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--pool", type=int, default=600)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--init", type=int, default=8)
    ap.add_argument("--n-test", type=int, default=300)
    ap.add_argument("--norm-input", action="store_true")
    ap.add_argument("--strong-aug", action="store_true")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default="results")
    ap.add_argument("--tag", default="")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in range(a.seeds):
        torch.manual_seed(seed)
        x, y, info = make_dataset(a.pool, seed=seed, return_info=True)
        enc = Encoder(norm_input=a.norm_input)
        hist = pretrain(enc, x, epochs=a.epochs, seed=seed, strong=a.strong_aug,
                        device=a.device)
        msg = (f"contrastive loss {hist[0]:.3f} -> {hist[-1]:.3f}" if hist
               else "random-init encoder (no pretraining)")
        print(f"seed {seed}: {msg}", flush=True)
        emb = embed(enc, x)
        evals = build_eval_sets(enc, seed, n=a.n_test)
        for s in STRATEGIES:
            for r in run_loop(emb, y, evals, s, a.init, a.batch, a.rounds, seed,
                              costs=info["cost"]):
                rows.append({"strategy": s, "seed": seed, **r})
    name = f"results{a.tag}"
    with open(out / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 4, figsize=(19, 4))
    for ax, m in zip(axes[:3], METRICS):
        for s in STRATEGIES:
            c = curves(rows, s, m)
            nl = curves(rows, s, "n_labeled").mean(0)
            ax.plot(nl, c.mean(0), marker="o", label=s)
            ax.fill_between(nl, c.mean(0) - c.std(0), c.mean(0) + c.std(0), alpha=0.1)
        ax.set_title(m)
        ax.set_xlabel("labels")
        ax.set_ylabel("accuracy")
    for s in STRATEGIES:
        ax = axes[3]
        ax.plot(curves(rows, s, "cum_cost").mean(0), curves(rows, s, "in_dist").mean(0),
                marker="o", label=s)
    axes[3].set_title("in_dist vs cumulative (assumed) annotation cost")
    axes[3].set_xlabel("cost units")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=110)

    strategies = list(STRATEGIES)
    md = ["## Accuracy\n", markdown_summary(rows, strategies, METRICS),
          "\n## Expected calibration error (lower is better)\n",
          markdown_summary(rows, strategies, [f"{m}_ece" for m in METRICS]),
          "\n## Mean top-label confidence (compare with accuracy: overconfidence under shift)\n",
          markdown_summary(rows, ["random"], [f"{m}_conf" for m in METRICS])]
    (out / f"{name}_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return rows


if __name__ == "__main__":
    main()
