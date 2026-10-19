# microscopy-active-learning

[![ci](https://github.com/iamvisheshsrivastava/microscopy-active-learning/actions/workflows/ci.yml/badge.svg)](https://github.com/iamvisheshsrivastava/microscopy-active-learning/actions/workflows/ci.yml)

A small, honest prototype: self-supervised embeddings of synthetic microstructure images, plus
pool-based active learning, a property surrogate with uncertainty, and SEM+EBSD cross-modal
pretraining, all evaluated under scale shift and instrument shift. **This is a toy pipeline, not research.**
The data is synthetic, the scale is tiny, and most results below are negative or mixed. They show
what a real study has to beat, not that anything works.

## Problem

Labelling micrographs (phase, texture, defect type, properties) needs expert time. Given a pool of
unlabeled images: which should be labeled first, how reliable are the model's uncertainties, do
representations survive a change of magnification or instrument, and can a second modality (EBSD) help
an SEM-only workflow? This repo is the smallest seeded, reproducible harness that asks these questions,
meant to be re-run on real data (see Roadmap).

## How it maps to the Jülich IAS-9 topic

| PhD topic | Here |
|---|---|
| Multi-scale representation learning | SimCLR with 15-100% random-resized crops; magnification-shift test set |
| Multi-modal (SEM, EBSD) | Registered synthetic SEM+EBSD pairs; CLIP-style cross-modal pretraining; SEM→EBSD retrieval |
| Robust to scale / modality / instrument shift | Scale shift (x1.5), instrument shift (contrast, noise, blur, offset); an input-normalisation + strong-augmentation variant |
| Active learning / experimental design under cost and uncertainty | 5 query strategies incl. an assumed-cost-aware one; learning curves vs labels and vs cost; paired significance tests |
| Surrogates from representations to properties | GP on embeddings predicting a synthetic hardness; active learning for regression; interval coverage |
| Uncertainty modelling | ECE and confidence for the classifier; 90% interval coverage for the GP |
| Open-source research software | Seeded CLIs, 25 tests, CI, group-aware splits and a metadata-CSV loader for real data |

## Quick start

```bash
pip install torch                      # CPU is fine; --device cuda works if available
pip install -e ".[dev]"
pytest -q                              # 25 tests, ~35 s

python scripts/run_experiment.py --tag _baseline                             # ~16 min, 10 seeds
python scripts/run_experiment.py --norm-input --strong-aug --tag _robust     # instrument-robustness variant
python scripts/run_experiment.py --epochs 0 --norm-input --tag _noprtrain    # no-pretraining ablation
python scripts/run_surrogate_al.py                                           # property surrogate AL
python scripts/run_multimodal.py                                             # SEM+EBSD cross-modal
```

Each run writes `results/<name>.csv` (every seed/round), `.png` curves, and `_summary.md` tables.
Layout: `src/maldl/{data,models,training,active,eval}`, `scripts/`, `tests/`.

## Synthetic data (all assumptions, no real physics)

4 texture classes (fine grains, coarse grains, lamellar, precipitates), 64x64, Voronoi grains with
noise and blur; an EBSD-like 2-channel orientation map per sample (boundaries and precipitates
non-indexed); a scalar "hardness" from a Hall-Petch-like formula using the *physical* grain size (so it is
magnification-independent); an annotation cost `1 + n_grains/20` (assumed). Scale shift = features x1.5.
Instrument shift = a second `Source` with lower contrast, more noise, more blur, and a brightness offset.

## Setup of the reported runs

Pool of 600 per seed, 3-conv-block CNN encoder (128-d), 15 NT-Xent epochs on the unlabeled pool, then
frozen. Classification head: logistic regression. Start with 8 labels, +8 per round, 8 rounds (72 labels).
Test sets: 300 images each, from seeds disjoint from training. **10 seeds** for classification and surrogate,
5 for the multimodal run. Nothing was tuned after seeing results. Significance: paired Wilcoxon on the
per-seed area under the learning curve (ALC) versus `random`; **no multiple-comparison correction**, so
isolated p≈0.03 values should be treated as noise.

## Results

Full tables, including ECE and ALC differences: `results/*_summary.md`.

### 1. Active learning, baseline (weak augmentation) — accuracy at 72 labels, mean±std over 10 seeds

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| random | 0.888±0.046 | 0.534±0.126 | 0.249±0.005 |
| uncertainty | 0.934±0.041 | 0.510±0.116 | 0.250±0.001 |
| diversity | 0.889±0.047 | 0.535±0.094 | 0.252±0.018 |
| hybrid | 0.928±0.050 | 0.514±0.144 | 0.252±0.011 |
| cost_uncertainty | 0.917±0.039 | 0.490±0.110 | 0.248±0.004 |

ALC difference vs random: in-distribution, only `hybrid` is nominally better (+0.020, p=0.03; uncorrected).
On **scale shift, uncertainty sampling is significantly *worse* than random** (−0.040, p=0.01;
cost-aware −0.064, p<0.01). On instrument shift everything is at chance (0.25 for 4 classes).

### 2. Calibration under shift (baseline, `random` strategy)

| | in_dist | scale_shift | source_shift |
|---|---|---|---|
| accuracy | 0.888 | 0.534 | 0.249 |
| mean confidence | 0.893 | 0.849 | 0.953 |
| ECE | 0.041 | 0.317 | 0.704 |

The classifier is well calibrated in-distribution and **badly overconfident under shift** (95% confident,
25% correct on the shifted instrument). Entropy-based acquisition inherits this: it also raised ECE on scale
shift (+0.070, p<0.01). Calibrated or shift-aware uncertainty is a real open problem here, not a solved one.

### 3. Instrument-robustness variant (per-image normalisation + strong augmentation) — 10 seeds

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| random | 0.756±0.051 | 0.535±0.068 | 0.369±0.082 |
| uncertainty | 0.779±0.067 | 0.492±0.076 | 0.387±0.069 |
| diversity | 0.790±0.042 | 0.516±0.067 | 0.385±0.080 |
| hybrid | 0.790±0.056 | 0.495±0.070 | 0.380±0.077 |
| cost_uncertainty | 0.761±0.078 | 0.476±0.057 | 0.337±0.070 |

Instrument-shift accuracy rises from chance (0.25) to ~0.37, which is still poor, and in-distribution accuracy
**drops** from ~0.89 to ~0.76. This is a trade-off, not a fix. Scale-shift behaviour is unchanged (uncertainty-based
strategies still lose to random there).

### 4. Does contrastive pretraining help? (it is not clear)

No-pretraining ablation (random-init encoder with input normalisation, weak aug, 10 seeds): `random` strategy
in_dist 0.844±0.019, scale 0.557±0.049, source 0.278±0.040. The baseline contrastive encoder reaches 0.888 in-distribution
(but has no input normalisation, so this is not a perfectly controlled comparison), while the
robustness-variant contrastive encoder (0.756) is **worse than the random-init encoder** (0.844) in-distribution.
The SimCLR stage has not shown a clear benefit at this scale; it needs longer training, a bigger pool and harder data
before any claim.

### 5. Cost-aware acquisition (assumed cost model)

Mean total cost to label 72 samples (baseline run): random 174, diversity 152, hybrid 141, uncertainty 137, cost_uncertainty 131.
Uncertainty sampling already prefers cheaper (coarse-grain) images in this synthetic setup, so
`cost_uncertainty` saves only ~4% more cost than plain uncertainty and has lower accuracy (0.917 vs 0.934).
No evidence that explicit cost-awareness helps here; the result depends entirely on the invented cost model.

### 6. Property surrogate (GP on embeddings) with active learning — 10 seeds, 72 labels

| strategy | in-dist RMSE | in-dist R² | in-dist 90% coverage | source-shift 90% coverage |
|---|---|---|---|---|
| random | 21.6±1.7 | 0.700±0.047 | 0.885 | 0.691 |
| uncertainty | 21.3±1.4 | 0.709±0.037 | 0.865 | 0.708 |
| diversity | 20.9±1.8 | 0.717±0.048 | 0.887 | 0.659 |
| hybrid | 21.2±1.5 | 0.711±0.041 | 0.874 | 0.657 |
| cost_uncertainty | 25.2±3.9 | 0.582±0.132 | 0.825 | 0.785 |

No active strategy is significantly better than random for the surrogate (uncertainty, diversity and hybrid: p>0.2 in distribution; `cost_uncertainty` is worse, p=0.05, and clearly worse under scale shift). Intervals are
close to nominal in-distribution (~0.88 vs 0.90) and **under-cover under shift** (~0.66–0.71). R² under scale shift is ~0.2
and about 0 under instrument shift: the representation does not transfer, so the surrogate does not either.

### 7. SEM+EBSD cross-modal pretraining (5 seeds; SEM-only at test time)

Few-label downstream results (mean over 5 random label draws per seed):

| encoder | labels | in_dist acc | in_dist R² | source_shift acc |
|---|---|---|---|---|
| random_init | 16 | 0.677±0.048 | 0.526±0.086 | 0.276±0.006 |
| simclr_sem | 16 | 0.615±0.039 | 0.560±0.055 | 0.345±0.031 |
| clip_sem_ebsd | 16 | 0.687±0.019 | 0.660±0.035 | 0.313±0.032 |
| random_init | 48 | 0.839±0.031 | 0.701±0.061 | 0.277±0.023 |
| simclr_sem | 48 | 0.716±0.023 | 0.640±0.046 | 0.368±0.057 |
| clip_sem_ebsd | 48 | 0.807±0.019 | 0.742±0.012 | 0.334±0.031 |

Cross-modal pretraining gives the best property R² in-distribution (0.74 vs 0.64 SimCLR and 0.70 random-init at 48 labels), but it does not beat a random-init encoder on classification accuracy, and
all encoders are poor under instrument shift. With 5 seeds I make no significance claim. Retrieval on 300 held-out pairs: exact-pair recall@1 0.005 (chance 0.003) and recall@10 0.059 (chance 0.033) are near chance, while the retrieved EBSD map has the right class 45% of the time (chance 25%; 29% under instrument shift). The two modalities share only coarse
structure here, so the alignment learned is coarse.

## Limitations

- **Synthetic data only.** Classes, property and cost are invented, easy to separate, and share the generator with the test sets. Nothing here is evidence about real microscopy.
- **Small scale.** 600-image pool, 64×64 images, 3-block CNN, 15 epochs, 5–10 seeds. Differences of a few points are within noise; p-values are uncorrected.
- **Scale shift is partly label-ambiguous by design** (a magnified fine texture looks coarse), so some loss is unavoidable without magnification metadata.
- **Mixed-up comparisons.** The no-pretraining ablation differs from the baseline in input normalisation; I did not run the full 2×2.
- **Cross-modal setup is toy:** EBSD is a deterministic function of the same latent grains; no flips/rotations in cross-modal training (orientation encoding); no real registration error.
- The real-data loaders (`data/folder.py`) and group splits are unit-tested on synthetic files only.
- No hyperparameter search, no pretrained-backbone baseline, no GPU runs yet.

## Roadmap (real data first)

Tracked as [issues #1-#9](https://github.com/iamvisheshsrivastava/microscopy-active-learning/issues).

1. UHCSDB (NIST, CC BY-SA 3.0) and the Aachen–Heerlen steel SEM set: sample-grouped splits (`data/splits.py`), leave-one-source-out evaluation, real magnification metadata.
2. Real SEM+EBSD pairs (e.g. the Georgia Tech dual-phase steel set, if its sample correspondence holds, or IAS-9 partner data) in place of the synthetic pair generator.
3. Scale-conditioned / scale-equivariant representation; stronger backbones (ViT, DINOv2-style) with pretrained and supervised baselines on GPU.
4. Calibrated, shift-aware uncertainty (ensembles, conformal) and cost-aware batch acquisition (BADGE, BALD) with measured acquisition costs.
5. Surrogate to real properties (hardness, strength) with calibrated uncertainty.

## License

MIT
