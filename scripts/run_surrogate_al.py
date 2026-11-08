"""Active learning for a property surrogate (GP on SimCLR embeddings), with uncertainty."""
import argparse
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.active.loop import run_regression_loop  # noqa: E402
from maldl.data.synthetic import make_dataset  # noqa: E402
from maldl.eval.report import plot_learning_curves, write_rows_csv  # noqa: E402
from maldl.eval.shift import build_eval_sets  # noqa: E402
from maldl.eval.stats import markdown_summary  # noqa: E402
from maldl.models.encoder import Encoder  # noqa: E402
from maldl.training.contrastive import embed, pretrain  # noqa: E402

STRATS = ["random", "uncertainty", "diversity", "hybrid", "cost_uncertainty"]
SETS = ["in_dist", "scale_shift", "source_shift"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--pool", type=int, default=600)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--init", type=int, default=8)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default="results")
    ap.add_argument("--tag", default="_surrogate")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in range(a.seeds):
        torch.manual_seed(seed)
        x, _, info = make_dataset(a.pool, seed=seed, return_info=True)
        enc = Encoder(norm_input=True)
        pretrain(enc, x, epochs=a.epochs, seed=seed, strong=True, device=a.device)
        emb = embed(enc, x)
        evals = build_eval_sets(enc, seed)
        print(f"seed {seed} done", flush=True)
        for s in STRATS:
            for r in run_regression_loop(emb, info["property"], evals, s, a.init, a.batch,
                                         a.rounds, seed, costs=info["cost"]):
                rows.append({"strategy": s, "seed": seed, **r})
    name = f"results{a.tag}"
    write_rows_csv(rows, out / f"{name}.csv")

    plot_learning_curves(rows, SETS, STRATS, out / f"{name}.png",
                         metric_columns=[f"{st}_rmse" for st in SETS],
                         titles=[f"{st}: property RMSE (lower is better)" for st in SETS])
    md = ["## Property RMSE (HV-like units, lower is better)\n",
          markdown_summary(rows, STRATS, [f"{m}_rmse" for m in SETS]),
          "\n## Property R2 (higher is better)\n",
          markdown_summary(rows, STRATS, [f"{m}_r2" for m in SETS]),
          "\n## 90% interval coverage (nominal 0.90)\n",
          markdown_summary(rows, STRATS, [f"{m}_cov90" for m in SETS])]
    (out / f"{name}_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
