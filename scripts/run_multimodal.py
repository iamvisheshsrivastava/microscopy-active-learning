"""Does pairing SEM with EBSD during pretraining help SEM-only downstream tasks?

Encoders compared (all evaluated on SEM images only, at test time EBSD is absent):
  random_init | simclr_sem (SEM-only SimCLR) | clip_sem_ebsd (cross-modal, SEM+EBSD pairs)
Downstream: few-label class accuracy (logistic regression) and property regression (GP),
in-distribution and under instrument shift. Also SEM->EBSD retrieval recall@1.
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.data.synthetic import SOURCE_A, SOURCE_B, make_paired_dataset  # noqa: E402
from maldl.eval.calibration import interval_coverage  # noqa: E402
from maldl.models.encoder import Encoder  # noqa: E402
from maldl.models.surrogate import GPSurrogate  # noqa: E402
from maldl.training.contrastive import embed, pretrain  # noqa: E402
from maldl.training.crossmodal import (embed_projected, pretrain_crossmodal,  # noqa: E402
                                           retrieval_class_match, retrieval_recall)

ENCODERS = ["random_init", "simclr_sem", "clip_sem_ebsd"]


def downstream(pool_emb, y, prop, test, n_labels, rng, draws=5):
    """Mean over `draws` random labeled subsets. test: {set: (emb, y, prop)}."""
    res = {}
    for _ in range(draws):
        idx = rng.choice(len(y), size=n_labels, replace=False)
        sc = StandardScaler().fit(pool_emb[idx])
        clf = LogisticRegression(max_iter=500).fit(sc.transform(pool_emb[idx]), y[idx])
        gp = GPSurrogate(pool_emb).fit(pool_emb[idx], prop[idx])
        for name, (e, ty, tp) in test.items():
            m, s = gp.predict(e)
            for k, v in (("acc", float((clf.predict(sc.transform(e)) == ty).mean())),
                         ("r2", float(r2_score(tp, m))),
                         ("cov90", interval_coverage(tp, m, s))):
                res.setdefault(f"{name}_{k}", []).append(v)
    return {k: float(np.mean(v)) for k, v in res.items()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--pool", type=int, default=600)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--labels", type=int, nargs="+", default=[16, 48])
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default="results")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in range(a.seeds):
        torch.manual_seed(seed)
        sem, ebsd, y, info = make_paired_dataset(a.pool, seed)
        tests = {}
        for i, (nm, src) in enumerate([("in_dist", SOURCE_A), ("source_shift", SOURCE_B)]):
            ts, te, ty, ti = make_paired_dataset(300, 10_000 + seed * 10 + i, source=src)
            tests[nm] = (ts, te, ty, ti["property"])
        encs = {"random_init": Encoder(norm_input=True)}
        encs["simclr_sem"] = Encoder(norm_input=True)
        pretrain(encs["simclr_sem"], sem, epochs=a.epochs, seed=seed, strong=True,
                 device=a.device)
        e_sem, e_ebsd = Encoder(norm_input=True), Encoder(in_ch=2)
        h = pretrain_crossmodal(e_sem, e_ebsd, sem, ebsd, epochs=a.epochs, seed=seed,
                                strong=True, device=a.device)
        encs["clip_sem_ebsd"] = e_sem
        print(f"seed {seed}: cross-modal loss {h[0]:.3f} -> {h[-1]:.3f}", flush=True)
        for en, enc in encs.items():
            pool = embed(enc, sem)
            test = {nm: (embed(enc, t[0]), t[2], t[3]) for nm, t in tests.items()}
            rec = {}
            if en == "clip_sem_ebsd":
                te = tests["in_dist"]
                for nm in ("in_dist", "source_shift"):
                    t = tests[nm]
                    a_, b_ = embed_projected(e_sem, t[0]), embed_projected(e_ebsd, t[1])
                    rec[f"retrieval_r1_{nm}"] = retrieval_recall(a_, b_, 1)
                    rec[f"retrieval_r10_{nm}"] = retrieval_recall(a_, b_, 10)
                    rec[f"retrieval_cls_{nm}"] = retrieval_class_match(a_, b_, t[2])
            for nl in a.labels:
                rng = np.random.default_rng(1000 * seed + nl)
                rows.append({"encoder": en, "seed": seed, "n_labels": nl, **rec,
                             **downstream(pool, y, info["property"], test, nl, rng)})
    keys = sorted({k for r in rows for k in r})
    with open(out / "results_multimodal.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

    md = [f"Mean±std over {a.seeds} seeds (each seed = mean of 5 random label draws). "
          f"Retrieval chance = 1/300 = 0.003.\n"]
    cols = ["in_dist_acc", "source_shift_acc", "in_dist_r2", "source_shift_r2",
            "in_dist_cov90", "source_shift_cov90"]
    for nl in a.labels:
        md += [f"### {nl} labels\n", "| encoder | " + " | ".join(cols) + " |",
               "|---|" + "---|" * len(cols)]
        for en in ENCODERS:
            rs = [r for r in rows if r["encoder"] == en and r["n_labels"] == nl]
            md.append(f"| {en} | " + " | ".join(
                f"{np.mean([r[c] for r in rs]):.3f}±{np.std([r[c] for r in rs]):.3f}"
                for c in cols) + " |")
        md.append("")
    rs = [r for r in rows if r["encoder"] == "clip_sem_ebsd" and r["n_labels"] == a.labels[0]]
    md += ["Cross-modal SEM->EBSD retrieval on 300 held-out pairs (chance: R@1 0.003, "
           "R@10 0.033, class-match 0.25):\n", "| test set | R@1 | R@10 | top-1 class match |",
           "|---|---|---|---|"]
    for nm in ("in_dist", "source_shift"):
        md.append(f"| {nm} | " + " | ".join(
            f"{np.mean([r[f'retrieval_{k}_{nm}'] for r in rs]):.3f}" for k in ("r1", "r10", "cls"))
            + " |")
    (out / "results_multimodal_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
