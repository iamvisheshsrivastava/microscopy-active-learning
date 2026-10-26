"""Active learning on REAL micrographs (UHCSDB) with specimen-grouped splits and real shifts.

Each seed: split specimens (not images) into pool/test groups. Pool = SE-detector, low-magnification
images of pool specimens (labels hidden until queried). Test sets use held-out specimens only:
  in_dist        SE detector, low magnification
  mag_shift      SE detector, high magnification   (real magnification shift)
  detector_shift BSE detector                       (real instrument/contrast shift)
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
from maldl.data.splits import group_split  # noqa: E402
from maldl.data.uhcsdb import load_uhcsdb  # noqa: E402
from maldl.eval.stats import curves, markdown_summary  # noqa: E402
from maldl.models.classical import classical_embed  # noqa: E402
from maldl.models.encoder import Encoder  # noqa: E402
from maldl.training.contrastive import embed, pretrain  # noqa: E402

SETS = ["in_dist", "mag_shift", "detector_shift"]
STRATS = ["random", "uncertainty", "diversity", "hybrid"]


def make_split(meta, seed, test_frac, min_eval, min_pool, mag_split):
    """Retry group splits (deterministically) until every eval set and the pool are big enough."""
    # images without a specimen id cannot be grouped safely -> excluded entirely
    valid = np.array([not g.startswith("nokey_") for g in meta["group"]])
    vidx = np.flatnonzero(valid)
    se, bse = meta["detector"] == "SE", meta["detector"] == "BSE"
    low = meta["magnification"] <= mag_split
    high = meta["magnification"] > mag_split
    for attempt in range(200):
        tr, te = group_split(meta["group"][vidx], test_frac, seed=seed * 1000 + attempt)
        trm, tem = np.zeros(len(se), bool), np.zeros(len(se), bool)
        trm[vidx[tr]], tem[vidx[te]] = True, True
        pool = np.flatnonzero(trm & se & low)
        ev = {"in_dist": np.flatnonzero(tem & se & low), "mag_shift": np.flatnonzero(tem & se & high),
              "detector_shift": np.flatnonzero(tem & bse)}
        if len(pool) >= min_pool and all(len(v) >= min_eval for v in ev.values()):
            assert not set(meta["group"][pool]) & set(meta["group"][np.concatenate(list(ev.values()))])
            return pool, ev
    raise RuntimeError(f"no valid split for seed {seed}; relax --min-eval/--min-pool")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default="data/raw/uhcs_mirror")
    ap.add_argument("--size", type=int, default=64)
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--encoder", choices=["contrastive", "random", "classical", "pretrained"],
                    default="contrastive")
    ap.add_argument("--backbone", default="facebook/dinov2-small",
                    help="Hugging Face model id for --encoder pretrained (downloaded at run time)")
    ap.add_argument("--norm-input", action="store_true")
    ap.add_argument("--strong-aug", action="store_true")
    ap.add_argument("--init", type=int, default=14)
    ap.add_argument("--batch", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--test-frac", type=float, default=0.35)
    ap.add_argument("--min-eval", type=int, default=20)
    ap.add_argument("--min-pool", type=int, default=150)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default="results")
    ap.add_argument("--tag", default="_real")
    a = ap.parse_args(argv)
    x, meta, classes = load_uhcsdb(a.data_root, a.size, cache_dir="data/cache")
    nc = len(classes)
    mag_split = float(np.nanmedian(meta["magnification"]))
    print(f"{len(x)} images, {len(set(meta['group']))} specimens, classes={classes}, "
          f"median mag split={mag_split:.0f}x", flush=True)
    rows, sizes, majority = [], [], []
    # deterministic, training-free embeddings are computed once for all images
    all_emb = None
    if a.encoder == "classical":
        all_emb = classical_embed(x)
    elif a.encoder == "pretrained":
        from maldl.models.backbone import PretrainedBackbone
        all_emb = PretrainedBackbone(a.backbone, a.device, a.size)(x)
        print(f"{a.backbone}: embeddings {all_emb.shape}", flush=True)
    for seed in range(a.seeds):
        torch.manual_seed(seed)
        pool, ev = make_split(meta, seed, a.test_frac, a.min_eval, a.min_pool, mag_split)
        enc = Encoder(norm_input=a.norm_input)
        if all_emb is not None:
            print(f"seed {seed}: pool {len(pool)}, {a.encoder} features", flush=True)
            emb_pool = all_emb[pool]
            evals = {k: (all_emb[i], meta["y"][i]) for k, i in ev.items()}
        else:
            if a.encoder == "contrastive":
                hist = pretrain(enc, x[pool], epochs=a.epochs, seed=seed, strong=a.strong_aug,
                                device=a.device)
                print(f"seed {seed}: pool {len(pool)}, contrastive loss "
                      f"{hist[0]:.2f}->{hist[-1]:.2f}, eval sizes "
                      f"{ {k: len(v) for k, v in ev.items()} }", flush=True)
            else:
                enc.eval()
                print(f"seed {seed}: pool {len(pool)}, {a.encoder} features", flush=True)
            emb_pool = embed(enc, x[pool])
            evals = {k: (embed(enc, x[i]), meta["y"][i]) for k, i in ev.items()}
        maj = np.bincount(meta["y"][pool], minlength=nc).argmax()
        majority.append({k: float((meta["y"][i] == maj).mean()) for k, i in ev.items()})
        sizes.append({k: len(i) for k, i in ev.items()} | {"pool": len(pool)})
        for s in STRATS:
            for r in run_loop(emb_pool, meta["y"][pool], evals, s, a.init, a.batch, a.rounds,
                              seed, num_classes=nc):
                rows.append({"strategy": s, "seed": seed, **r})
    name = f"results{a.tag}"
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / f"{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, m in zip(axes, SETS):
        for s in STRATS:
            c = curves(rows, s, m)
            nl = curves(rows, s, "n_labeled").mean(0)
            ax.plot(nl, c.mean(0), marker="o", label=s)
            ax.fill_between(nl, c.mean(0) - c.std(0), c.mean(0) + c.std(0), alpha=0.1)
        ax.axhline(np.mean([mj[m] for mj in majority]), ls=":", c="gray", label="majority class")
        ax.set_title(f"UHCSDB {m}")
        ax.set_xlabel("labels")
        ax.set_ylabel("accuracy")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=110)
    mean_sz = {k: float(np.mean([s[k] for s in sizes])) for k in sizes[0]}
    md = [f"Encoder: {a.encoder} (norm_input={a.norm_input}, strong_aug={a.strong_aug}); "
          f"{nc} classes; mean sizes: " + ", ".join(f"{k}={v:.0f}" for k, v in mean_sz.items()),
          "Majority-class accuracy (predict most frequent pool class): " + ", ".join(
              f"{k}={np.mean([m[k] for m in majority]):.3f}" for k in SETS) + "\n",
          "## Accuracy\n", markdown_summary(rows, STRATS, SETS),
          "\n## Balanced accuracy\n", markdown_summary(rows, STRATS, [f"{m}_bacc" for m in SETS]),
          "\n## Expected calibration error (lower is better)\n",
          markdown_summary(rows, STRATS, [f"{m}_ece" for m in SETS])]
    (out / f"{name}_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
