"""Seeded experiment: random vs uncertainty vs diversity vs hybrid on frozen embeddings."""
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
from maldl.models.encoder import Encoder  # noqa: E402
from maldl.training.contrastive import embed, pretrain  # noqa: E402

METRICS = ["in_dist", "scale_shift", "source_shift"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--pool", type=int, default=600)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--init", type=int, default=8)
    ap.add_argument("--n-test", type=int, default=300)
    ap.add_argument("--out", default="results")
    ap.add_argument("--tag", default="")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in range(a.seeds):
        torch.manual_seed(seed)
        x, y = make_dataset(a.pool, seed=seed)
        enc = Encoder()
        hist = pretrain(enc, x, epochs=a.epochs, seed=seed)
        msg = (f"contrastive loss {hist[0]:.3f} -> {hist[-1]:.3f}" if hist
               else "random-init encoder (no pretraining)")
        print(f"seed {seed}: {msg}", flush=True)
        emb = embed(enc, x)
        evals = build_eval_sets(enc, seed, n=a.n_test)
        for s in STRATEGIES:
            for r in run_loop(emb, y, evals, s, a.init, a.batch, a.rounds, seed):
                rows.append({"strategy": s, "seed": seed, **r})
    name = f"results{a.tag}"
    with open(out / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    summary = {}
    for ax, m in zip(axes, METRICS):
        for s in STRATEGIES:
            rs = [r for r in rows if r["strategy"] == s]
            nl = sorted({r["n_labeled"] for r in rs})
            mat = np.array([[r[m] for r in rs if r["n_labeled"] == k] for k in nl])
            mean, sd = mat.mean(1), mat.std(1)
            ax.plot(nl, mean, marker="o", label=s)
            ax.fill_between(nl, mean - sd, mean + sd, alpha=0.12)
            summary[(s, m)] = (mean[-1], sd[-1], mean.mean())
        ax.set_title(m)
        ax.set_xlabel("labels")
        ax.set_ylabel("accuracy")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=120)
    print(f"\nFinal-round accuracy (mean±std over {a.seeds} seeds), curve-mean in parens")
    for s in STRATEGIES:
        print(f"{s:12s}", " | ".join(
            f"{m}: {summary[(s, m)][0]:.3f}±{summary[(s, m)][1]:.3f} ({summary[(s, m)][2]:.3f})"
            for m in METRICS))
    return rows


if __name__ == "__main__":
    main()
