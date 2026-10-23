"""Regenerate every results/*_summary.md from the saved CSVs (Holm-adjusted p, bootstrap CIs).

No experiment is rerun. Any text before the first '## ' heading in an existing summary
(encoder / majority-class header lines) is preserved.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.eval.stats import markdown_summary  # noqa: E402

META = {"strategy", "seed", "round", "n_labeled", "cum_cost"}
FAMILIES = [("", "Accuracy"), ("_bacc", "Balanced accuracy"), ("_ece", "Expected calibration error (lower is better)"),
            ("_rmse", "Property RMSE (lower is better)"), ("_r2", "Property R2 (higher is better)"),
            ("_cov90", "90% interval coverage (nominal 0.90)")]


def load(path):
    rows = []
    for r in csv.DictReader(open(path, newline="")):
        rows.append({k: (v if k == "strategy" else float(v)) for k, v in r.items()})
        rows[-1]["seed"], rows[-1]["round"] = int(rows[-1]["seed"]), int(rows[-1]["round"])
    return rows


def main(results="results"):
    for path in sorted(Path(results).glob("results_*.csv")):
        if path.stem == "results_multimodal":
            continue  # different layout; summarised by run_multimodal.py
        rows = load(path)
        cols = [c for c in rows[0] if c not in META]
        suffixes = ("_bacc", "_ece", "_conf", "_rmse", "_r2", "_cov90")
        sets = [c for c in cols if not c.endswith(suffixes)] or sorted(
            {c.rsplit("_", 1)[0] for c in cols})
        strategies = list(dict.fromkeys(r["strategy"] for r in rows))
        summ = path.with_name(path.stem + "_summary.md")
        head = ""
        if summ.exists():
            old = summ.read_text(encoding="utf-8")
            head = old.split("## ", 1)[0].rstrip() + "\n\n" if not old.startswith("## ") else ""
        md = [head.rstrip(), ""] if head else []
        for suf, title in FAMILIES:
            metrics = [f"{s}{suf}" for s in sets if f"{s}{suf}" in cols]
            if metrics and (suf or not any(c.endswith("_rmse") for c in cols)):
                md += [f"## {title}\n", markdown_summary(rows, strategies, metrics), ""]
        summ.write_text("\n".join(md), encoding="utf-8")
        print("wrote", summ)


if __name__ == "__main__":
    main(*sys.argv[1:2])
