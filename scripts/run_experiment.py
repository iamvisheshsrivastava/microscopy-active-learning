"""Seeded classification experiment: query strategies on frozen embeddings.

Variants: default = baseline (weak augmentation, no input normalisation).
`--norm-input --strong-aug` = instrument-robustness variant.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.active.loop import run_loop  # noqa: E402
from maldl.active.strategies import STRATEGIES  # noqa: E402
from maldl.data.synthetic import make_dataset  # noqa: E402
from maldl.eval.report import plot_learning_curves, write_rows_csv  # noqa: E402
from maldl.eval.shift import build_eval_sets  # noqa: E402
from maldl.eval.stats import markdown_summary  # noqa: E402
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
    write_rows_csv(rows, out / f"{name}.csv")

    plot_learning_curves(rows, METRICS, list(STRATEGIES), out / f"{name}.png",
                         ylabel="accuracy", cost_metric="cum_cost",
                         cost_title="in_dist vs cumulative (assumed) annotation cost")

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
