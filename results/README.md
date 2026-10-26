# Results index

Every file here comes from a seeded run; `*_summary.md` are regenerated from the CSVs with
`python scripts/resummarize.py` (Holm-adjusted p-values, bootstrap CIs). Logs are `log_*.txt`.

| files | what | seeds | command tag |
|---|---|---|---|
| `results_baseline.*` | synthetic, weak aug, 5 strategies | 10 | `run_experiment.py --tag _baseline` |
| `results_robust.*` | synthetic, input norm + strong aug | 10 | `--norm-input --strong-aug --tag _robust` |
| `results_noprtrain.*` | synthetic, random-init encoder + norm | 10 | `--epochs 0 --norm-input --tag _noprtrain` |
| `results_surrogate.*` | synthetic property surrogate (GP) AL | 10 | `run_surrogate_al.py` |
| `results_multimodal.*` | synthetic SEM+EBSD cross-modal | 5 | `run_multimodal.py` (no significance tests) |
| `results_real_contrastive.*`, `_robust` | UHCSDB, 64 px, SimCLR (weak / strong aug + norm) | 10 | `run_real.py --epochs 60` |
| `results_real_random.*`, `_random_norm` | UHCSDB, 64 px, random-init CNN | 10 | `run_real.py --encoder random` |
| `results_real_classical64.*`, `_classical128` | UHCSDB, handcrafted features | 10 | `run_real.py --encoder classical [--size 128]` |
| `results_real_random128.*` | UHCSDB, 128 px, random-init CNN | 10 | `run_real.py --encoder random --size 128` |
| `results_real_dinov2_small.*`, `_dinov2_base` | UHCSDB, frozen DINOv2, 224 px, **GPU (Kaggle T4)** | 10 | `kaggle_submit.py --job pretrained` |
| `results_real_contrastive128.*` | UHCSDB, 128 px, SimCLR 30 epochs | **5** | `run_real.py --size 128 --seeds 5 --epochs 30` |

Real-data runs use specimen-grouped splits and exclude images without a specimen id; see the main README.
Files from an earlier iteration (5 seeds, pre-refactor code) were removed and are not comparable.

Second real source (Aachen-Heerlen; embeddings built on a Kaggle GPU with `kaggle_submit.py --job aachen`):

| files | what | seeds | command |
|---|---|---|---|
| `results_aachen_cls_{base,small}.*` | temperature (400/500 C), sample-type-grouped, tilt and cut-direction shifts | 10 | `run_aachen.py --task cls --backbone base` |
| `results_aachen_reg_{base,small}.*` | MA-island area fraction, GP surrogate | 10 | `run_aachen.py --task reg --backbone base` |
