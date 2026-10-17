# HANDOFF: microscopy-active-learning (for Claude Code)

Date: 2026-10-17. Nothing is built yet. This file is the full brief.

## Why this repo exists
Vishesh Srivastava (M.Sc. Data Science, TU Dortmund) is applying for the Jülich IAS-9 PhD:
multi-scale, multi-modal representation learning for SEM/TEM/EBSD microscopy, with active
learning / experimental design under cost and uncertainty. This repo is a small, honest
prototype he can link in the application. It is NOT research. Say so in the README.

## What was done so far
- Sandbox check: Python 3.13, numpy, sklearn, PIL, matplotlib present.
- pytest installed. torch installs from PyPI (the pytorch.org CPU index is blocked, so use plain `pip install torch`).
- Target folder created: C:\Users\sriva\Desktop\Projects\Personal Repositories\microscopy-active-learning
- No source code written yet.

## What to build (in this order)
1. `src/maldl/data/synthetic.py`: seeded synthetic microstructure generator (grains via Voronoi, phases, noise, blur). Classes = phase/texture types. Must run offline.
2. `src/maldl/data/folder.py`: loader for a real image folder (e.g. UHCSDB steel micrographs; check licence and availability first, do not bundle data).
3. `src/maldl/models/encoder.py`: small CNN encoder, embedding dim 128.
4. `src/maldl/training/contrastive.py`: SimCLR-style self-supervised training with multi-scale random-resized crops, so embeddings are scale-invariant.
5. `src/maldl/active/strategies.py`: random, uncertainty (entropy), diversity (k-center / k-means on embeddings), and a hybrid.
6. `src/maldl/active/loop.py`: pool-based loop (logistic-regression head on frozen embeddings), several seeds, learning curves.
7. `src/maldl/eval/shift.py`: evaluate under scale shift (train at one magnification, test at another) and source shift (different generator settings = a different "instrument").
8. `scripts/run_experiment.py`: seeded CLI producing a CSV plus a learning-curve PNG in `results/`.
9. `tests/`: shapes, seed determinism, strategy picks unique unlabeled indices, loop never relabels, a tiny end-to-end smoke test (CPU, under 60 s).
10. `.github/workflows/ci.yml` (pytest on CPU), `pyproject.toml`, `README.md`, `.gitignore`, `LICENSE` (MIT).

## Rules
- CPU only, fixed seeds, no downloads at test time.
- Report real numbers from real runs, including when active learning does NOT beat random. Do not tune until it looks good.
- README must have: problem, how it maps to the Jülich topic, quick start, results table, and a Limitations section (synthetic data, small scale, no EBSD, no property surrogate yet).
- Roadmap section in README: real UHCSDB data, multi-modal (SEM+EBSD) pairing, surrogate model from embeddings to a property, uncertainty calibration.
- Keep style close to his other repos (spec2program: seeded eval harness, pytest, CI).

## After building
- Run `pytest -q` and one full experiment; paste the real results into the README.
- `git init`, commit, and tell Vishesh. He will push to GitHub (account: iamvisheshsrivastava) himself.
- Commit messages: end with the attribution lines from the session settings if any.
