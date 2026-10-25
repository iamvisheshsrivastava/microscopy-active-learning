# Contributing

This is a small research-prototype repo. Issues and PRs are welcome, especially the ones labelled `good first issue`.

## Ground rules

- **Report real numbers.** Negative results stay in the README. Do not tune until an active-learning strategy looks better than random.
- **Seeds and statistics.** Experiments are seeded. Compare strategies with paired tests over seeds; use `scripts/resummarize.py`, which reports Holm-adjusted p-values and bootstrap CIs.
- **No data in git.** Raw datasets live in the gitignored `/data/` folder. `scripts/get_uhcsdb.py` fetches and verifies UHCSDB. Check a dataset's licence before using it.
- **Specimen-grouped splits for real data.** Never split real micrographs by image; use `maldl.data.splits.group_split`.
- **CPU-only tests, no downloads at test time.** `pytest -q` must stay fast and offline.

## Dev setup

```bash
pip install torch
pip install -e ".[dev]"
pytest -q
```

## Adding an experiment

1. Add or reuse a script in `scripts/`; write `results/<tag>.csv` plus a `_summary.md` (run `python scripts/resummarize.py`).
2. Update the README results with the real numbers, including any where the new method does not help.
3. Link or open an issue for the open question it addresses.
