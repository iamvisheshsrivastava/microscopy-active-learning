# Full results

Detailed tables for every experiment in the repository. The README has the short version; all numbers are regenerated from `results/*.csv` by `scripts/resummarize.py` (Holm-adjusted p-values and bootstrap CIs are in `results/*_summary.md`).

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

### 4. Does contrastive pretraining help?

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
| **DINOv2-small (frozen, 224 px)** | random | 0.722±0.068 | 0.569±0.131 | 0.666±0.178 |
| DINOv2-small | uncertainty | 0.718±0.058 | 0.575±0.073 | 0.664±0.169 |
| DINOv2-small | diversity | 0.732±0.061 | 0.601±0.097 | 0.664±0.179 |
| DINOv2-small | hybrid | 0.736±0.064 | 0.577±0.085 | 0.644±0.174 |
| **DINOv2-base (frozen, 224 px)** | random | 0.770±0.050 | 0.602±0.158 | 0.708±0.122 |
| DINOv2-base | uncertainty | 0.755±0.064 | 0.621±0.119 | 0.697±0.108 |
| DINOv2-base | diversity | 0.774±0.045 | 0.603±0.134 | 0.703±0.120 |
| DINOv2-base | hybrid | 0.772±0.059 | 0.641±0.147 | 0.737±0.140 |

**Pretrained backbones (GPU, Kaggle T4).** `python scripts/kaggle_submit.py --job pretrained` runs a private Kaggle GPU job that
clones this repo, downloads UHCSDB (hash-verified) and the DINOv2 weights from Hugging Face at run time, and fetches the results back. Same
specimen-grouped splits, seeds, heads and statistics as every row above, so rows are directly comparable. The frozen pretrained features
are the largest effect in this study: relative to the best from-scratch encoder, in-distribution accuracy rises from ~0.55-0.61 to 0.72 (small) / 0.77 (base),
magnification-shift from ~0.43 to 0.57-0.60, and **detector shift from ~0.30-0.40 (majority-class level) to 0.67-0.71**. Caveat: DINOv2 is pretrained on a very
large external natural-image corpus, so this measures the value of external pretraining and not of anything learned in this repo; weights are not fine-tuned.
Active learning still does not help: no strategy differs from random after Holm correction (smallest adjusted p 0.25, DINOv2-base `hybrid` under magnification shift, +0.053 ALC).

What this does and does not say:
- **The task is hard for this pipeline:** ~0.55 accuracy in-distribution against a 0.35 majority baseline; balanced accuracy is only ~0.3 (7 classes, strong imbalance).
- **No active strategy beats random anywhere.** Every in-distribution ALC difference vs random is within ±0.02 with p≥0.16. The one result that survives Holm correction is negative: `diversity` is worse than random under magnification shift with a random-init encoder (−0.073, Holm p=0.04). Raw p-values elsewhere are mostly not significant after correction.
- **Contrastive pretraining is not better than a random-init encoder** (in-dist 0.553 vs 0.563 for `random`).
- **Training-free handcrafted features are as good as the CNN, and image size matters more than the encoder.** Intensity/gradient/orientation/LBP-style histograms (`models/classical.py`, contrast-invariant, no learning) give in-dist accuracy 0.555±0.059 at 64 px (same as the CNN) and **0.608±0.072 (random) / 0.642±0.061 (hybrid) at 128 px**. The strategies are still indistinguishable from random (all Holm p=1.00 at 128 px). Detector shift stays near the majority rate (0.27-0.30 at 128 px). So the learned encoder is not earning its keep at this scale, and for the handcrafted features higher resolution helped by ~5 points and the CNN does not change that picture at 128 px either (in-dist `random`: random-init CNN 0.582±0.063 over 10 seeds; contrastive CNN, 30 epochs, 0.590±0.078 over only 5 seeds; handcrafted 0.608±0.072). All three encoders are within one standard deviation of each other, and no strategy is distinguishable from random (all Holm p≥0.56). Pretraining still has not shown a benefit; a stronger test needs far more unlabeled images or a pretrained backbone.
- **Detector shift (SE→BSE):** accuracy is about the majority-class rate or below (0.30), and with per-image normalisation it drops to 0.18-0.23, *below* the majority baseline. The normalisation/strong-augmentation trick that helped the synthetic instrument shift does **not** transfer to this real detector shift. The BSE test sets are small (~34 images from a few specimens), so these numbers are noisy.
- Conclusion: the synthetic benchmark is not predictive of real behaviour (active-learning "gains" and the robustness trick both failed to transfer). Representation quality dominates: a frozen pretrained backbone improves every shift setting substantially (see above), while the choice of query strategy does not matter at this pool size and label budget.


## Second real source: Aachen-Heerlen steel SEM (1,705 images, CC0)

**Data.** Iren et al., *Scientific Data* 2021 (doi:10.1038/s41597-021-00926-7), figshare collection doi:10.6084/m9.figshare.c.5185004.v1. Bainitic steels, 1024×768 SEM images at one magnification (4000x), 10 steel sample types, expert polygons around martensite-austenite (MA) islands. The archive's MD5 was verified. Images are downloaded and embedded on a GPU (`scripts/kaggle_submit.py --job aachen`), and only the embeddings stay local.

**Tasks and protocol (`scripts/run_aachen.py`).** All splits are grouped by steel sample type, so a test type is never seen in training. The pool is the perpendicular view of the vertical cut; the shifts are real acquisition changes from the metadata. 10 seeds, 10 initial labels, +10 per round, 8 rounds (90 labels), frozen DINOv2 features.

- `cls`: transformation temperature (400 vs 500 °C), binary.
- `reg`: MA area fraction per image (sum of polygon areas over image area), predicted with the GP surrogate.
- `in_dist` = held-out sample types, same view; `tilt_shift` = tilted view; `direction_shift` = horizontal cut.

**Classification, DINOv2-base, accuracy at 90 labels.** Majority class: 0.441 / 0.430 / 0.353.

| strategy | in_dist | tilt_shift | direction_shift |
|---|---|---|---|
| random | 0.494±0.102 | 0.589±0.150 | 0.465±0.118 |
| uncertainty | 0.497±0.096 | 0.533±0.064 | 0.463±0.127 |
| diversity | 0.497±0.076 | 0.528±0.107 | 0.445±0.098 |
| hybrid | 0.489±0.107 | 0.523±0.069 | 0.412±0.082 |

The temperature of unseen steel types is not recoverable from frozen DINOv2 features with a linear head: accuracy sits within a standard deviation of the majority-class rate, and no strategy differs from random.

**MA area fraction, DINOv2-base (GP surrogate), 90 labels.** Predict-the-mean RMSE: 0.077 / 0.074 / 0.075.

| strategy | in_dist RMSE | tilt_shift RMSE | direction_shift RMSE | in_dist R² | in_dist 90% coverage |
|---|---|---|---|---|---|
| random | 0.0569±0.0133 | 0.0651±0.0170 | 0.0545±0.0139 | 0.343±0.137 | 0.867 |
| uncertainty | 0.0596±0.0149 | 0.0679±0.0171 | 0.0595±0.0153 | 0.284±0.180 | 0.809 |
| diversity | 0.0576±0.0140 | 0.0670±0.0164 | 0.0572±0.0152 | 0.324±0.180 | 0.760 |
| hybrid | 0.0577±0.0142 | 0.0666±0.0150 | 0.0579±0.0161 | 0.324±0.179 | 0.753 |

The surrogate beats the mean predictor (R² about 0.34 in distribution, 0.39 under the cut-direction shift) but degrades under tilt (R² about 0.10). No acquisition strategy lowers the error. Diversity and hybrid selection reduce the 90% interval coverage from 0.87 (random) to 0.76 and 0.75 (Holm p=0.02 for both; uncertainty sampling gives 0.81, not significant). Points chosen for diversity are atypical, so the fitted GP intervals are too narrow for typical images. DINOv2-small gives the same picture (`results/results_aachen_*_small_*`).
