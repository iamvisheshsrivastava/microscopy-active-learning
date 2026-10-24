# microscopy-active-learning

[![ci](https://github.com/iamvisheshsrivastava/microscopy-active-learning/actions/workflows/ci.yml/badge.svg)](https://github.com/iamvisheshsrivastava/microscopy-active-learning/actions/workflows/ci.yml)

A small, honest prototype: self-supervised embeddings of microstructure images, plus
pool-based active learning, a property surrogate with uncertainty, and SEM+EBSD cross-modal
pretraining, evaluated under scale shift and instrument shift. Most experiments use a synthetic
generator; one section ([Real data: UHCSDB](#real-data-uhcsdb-961-steel-sem-micrographs)) runs the
same active-learning harness on real steel micrographs with specimen-grouped splits.
**This is a toy pipeline, not research.** The scale is tiny and most results below are negative or
mixed. They show what a real study has to beat, not that anything works.

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
| Open-source research software | Seeded CLIs, 29 tests, CI, `CITATION.cff`, group-aware splits and a metadata-CSV loader for real data |

## Quick start

```bash
pip install torch                      # CPU is fine; --device cuda works if available
pip install -e ".[dev]"
pytest -q                              # 29 tests, ~40 s

python scripts/run_experiment.py --tag _baseline                             # ~16 min, 10 seeds
python scripts/run_experiment.py --norm-input --strong-aug --tag _robust     # instrument-robustness variant
python scripts/run_experiment.py --epochs 0 --norm-input --tag _noprtrain    # no-pretraining ablation
python scripts/run_surrogate_al.py                                           # property surrogate AL
python scripts/run_multimodal.py                                             # SEM+EBSD cross-modal

# real data (see "Real data" below for where to get it)
python scripts/run_real.py --epochs 60 --tag _real_contrastive
python scripts/run_real.py --encoder classical --size 128 --tag _real_classical128   # handcrafted baseline

python scripts/get_uhcsdb.py           # clone the UHCSDB mirror (~580 MB) and verify SHA-256 hashes
python scripts/resummarize.py          # regenerate summaries with Holm p-values and bootstrap CIs
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
per-seed area under the learning curve (ALC) versus `random`, with 95% bootstrap CIs and **Holm-adjusted p-values
over each table's cells** (`scripts/resummarize.py` regenerates all `results/*_summary.md` from the CSVs). Raw p≈0.03 values
usually do not survive the correction; the text below quotes Holm values where it makes a claim. The multimodal table is
5 seeds with no tests.

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

ALC difference vs random, after Holm correction over each table's 9 cells (bootstrap CIs and adjusted p-values are in
`results/*_summary.md`): **nothing is better than random in-distribution** (`hybrid` +0.020, raw p=0.03, Holm p=0.27).
On scale shift uncertainty sampling looks worse than random (−0.040, raw p=0.01) but **does not survive correction**
(Holm p=0.15); the cost-aware variant does (−0.064, Holm p=0.02). On instrument shift everything is at chance (0.25 for 4 classes).

### 2. Calibration under shift (baseline, `random` strategy)

| | in_dist | scale_shift | source_shift |
|---|---|---|---|
| accuracy | 0.888 | 0.534 | 0.249 |
| mean confidence | 0.893 | 0.849 | 0.953 |
| ECE | 0.041 | 0.317 | 0.704 |

The classifier is well calibrated in-distribution and **badly overconfident under shift** (95% confident,
25% correct on the shifted instrument). Entropy-based acquisition inherits this: it also raised ECE on scale
shift (+0.070 ECE, Holm p=0.02). Calibrated or shift-aware uncertainty is a real open problem here, not a solved one.

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

No active strategy is significantly better than random for the surrogate (uncertainty, diversity and hybrid: raw p>0.2 in distribution; `cost_uncertainty` is clearly worse under scale shift, Holm p=0.02). Intervals are
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

## Real data: UHCSDB (961 steel SEM micrographs)

**Data.** UHCSDB (DeCost et al., *Integr. Mater. Manuf. Innov.* 6, 197-205, 2017, doi:10.1007/s40192-017-0097-0; CC BY 3.0 US).
The NIST host (`hdl.handle.net/11256/940`) did not respond when I tried it (HTTP 502/404), so I used the Zenodo-archived
GitHub mirror [rydia001/UHCS_micrographs_mirror](https://github.com/rydia001/UHCS_micrographs_mirror)
(doi:10.5281/zenodo.23050463). All 961 image files matched the mirror's SHA-256 manifest. I could not compare against NIST, so I
rely on the mirror's own manifest. Data is not committed; clone the mirror to `data/raw/uhcs_mirror`.

**Task.** 7-class *primary microconstituent* (spheroidite, network, pearlite, pearlite+spheroidite, spheroidite+widmanstatten,
martensite, pearlite+widmanstatten). Images are cropped (SEM info banner removed), centre-square-cropped and resized to 64×64.

**Protocol (`scripts/run_real.py`).**
- Splits are by **specimen**, never by image. Images without a specimen id (~160 of 961) are **excluded**, because unknown specimens cannot be kept apart safely.
- Pool: SE-detector, low-magnification images of pool specimens (magnification ≤ median 1473x). Test specimens are disjoint.
- Real shifts, using held-out specimens only: `mag_shift` = SE detector at high magnification; `detector_shift` = BSE detector.
- 10 seeds (different specimen splits); about 190 pool images, 128/107/34 test images (in-dist / mag-shift / detector-shift) on average.
- 14 initial labels, +10 per round, 8 rounds (94 labels). Same encoder, heads and statistics as above (Wilcoxon on ALC vs random, Holm-corrected within each table).
- Full tables incl. balanced accuracy and ECE: `results/results_real_*_summary.md`.

**Results, accuracy at 94 labels (mean±std over 10 seeds).** Majority-class accuracy is 0.348 / 0.170 / 0.300 on the three sets.

| encoder | strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|---|
| contrastive | random | 0.553±0.074 | 0.428±0.103 | 0.372±0.073 |
| contrastive | uncertainty | 0.545±0.052 | 0.397±0.083 | 0.343±0.091 |
| contrastive | diversity | 0.568±0.078 | 0.381±0.061 | 0.324±0.085 |
| contrastive | hybrid | 0.546±0.054 | 0.375±0.074 | 0.306±0.131 |
| random-init | random | 0.563±0.072 | 0.354±0.084 | 0.401±0.164 |
| random-init | uncertainty | 0.555±0.055 | 0.352±0.093 | 0.383±0.180 |
| random-init | diversity | 0.558±0.059 | 0.257±0.086 | 0.321±0.121 |
| random-init | hybrid | 0.571±0.048 | 0.331±0.078 | 0.358±0.205 |
| contrastive + norm + strong aug | random | 0.528±0.068 | 0.398±0.131 | 0.180±0.087 |
| random-init + norm | random | 0.549±0.056 | 0.417±0.080 | 0.226±0.152 |

What this does and does not say:
- **The task is hard for this pipeline:** ~0.55 accuracy in-distribution against a 0.35 majority baseline; balanced accuracy is only ~0.3 (7 classes, strong imbalance).
- **No active strategy beats random anywhere.** Every in-distribution ALC difference vs random is within ±0.02 with p≥0.16. The one result that survives Holm correction is negative: `diversity` is worse than random under magnification shift with a random-init encoder (−0.073, Holm p=0.04). Raw p-values elsewhere are mostly not significant after correction.
- **Contrastive pretraining is not better than a random-init encoder** (in-dist 0.553 vs 0.563 for `random`).
- **Training-free handcrafted features are as good as the CNN, and image size matters more than the encoder.** Intensity/gradient/orientation/LBP-style histograms (`models/classical.py`, contrast-invariant, no learning) give in-dist accuracy 0.555±0.059 at 64 px (same as the CNN) and **0.608±0.072 (random) / 0.642±0.061 (hybrid) at 128 px**. The strategies are still indistinguishable from random (all Holm p=1.00 at 128 px). Detector shift stays near the majority rate (0.27-0.30 at 128 px). So the learned encoder is not earning its keep at this scale, and for the handcrafted features higher resolution helped by ~5 points and the CNN does not change that picture at 128 px either (in-dist `random`: random-init CNN 0.582±0.063 over 10 seeds; contrastive CNN, 30 epochs, 0.590±0.078 over only 5 seeds; handcrafted 0.608±0.072). All three encoders are within one standard deviation of each other, and no strategy is distinguishable from random (all Holm p≥0.56). Pretraining still has not shown a benefit; a stronger test needs far more unlabeled images or a pretrained backbone.
- **Detector shift (SE→BSE):** accuracy is about the majority-class rate or below (0.30), and with per-image normalisation it drops to 0.18-0.23, *below* the majority baseline. The normalisation/strong-augmentation trick that helped the synthetic instrument shift does **not** transfer to this real detector shift. The BSE test sets are small (~34 images from a few specimens), so these numbers are noisy.
- Conclusion: the synthetic benchmark is not predictive of real behaviour (active-learning "gains" and the robustness trick both failed to transfer). A real study needs stronger representations (pretrained backbones, more pretraining data) before active learning can be meaningfully assessed.

## Limitations

- **Mostly synthetic.** Sections 1-7 use synthetic classes, property and cost that are invented, easy to separate, and share the generator with the test sets; the real-data section shows they do not predict real behaviour. The real-data run covers one dataset, one task (microconstituent classification, no EBSD, no properties) and ~190 pool images.
- **Small scale.** 600-image pool, 64×64 images, 3-block CNN, 15 epochs, 5–10 seeds. Differences of a few points are within noise; claims rely on Holm-corrected paired tests over 10 seeds (5 for the multimodal run, untested).
- **Scale shift is partly label-ambiguous by design** (a magnified fine texture looks coarse), so some loss is unavoidable without magnification metadata.
- **Mixed-up comparisons.** The no-pretraining ablation differs from the baseline in input normalisation; I did not run the full 2×2.
- **Cross-modal setup is toy:** EBSD is a deterministic function of the same latent grains; no flips/rotations in cross-modal training (orientation encoding); no real registration error.
- The UHCSDB loader and group splits are unit-tested on synthetic files; real-data runs use a third-party mirror (hash-verified against its own manifest only).
- Real-data images are 64×64 squares cropped from larger micrographs, losing fine detail and part of the field of view.
- No hyperparameter search, no pretrained-backbone baseline, no GPU runs yet.

## Roadmap (real data first)

Tracked as [issues #1-#9](https://github.com/iamvisheshsrivastava/microscopy-active-learning/issues).

1. ~~UHCSDB baseline with grouped splits~~ (done above). Next: the Aachen–Heerlen steel SEM set as a second source, larger images, leave-one-source-out evaluation.
2. Real SEM+EBSD pairs (e.g. the Georgia Tech dual-phase steel set, if its sample correspondence holds, or IAS-9 partner data) in place of the synthetic pair generator.
3. Scale-conditioned / scale-equivariant representation; stronger backbones (ViT, DINOv2-style) with pretrained and supervised baselines on GPU.
4. Calibrated, shift-aware uncertainty (ensembles, conformal) and cost-aware batch acquisition (BADGE, BALD) with measured acquisition costs.
5. Surrogate to real properties (hardness, strength) with calibrated uncertainty.

## License

MIT
