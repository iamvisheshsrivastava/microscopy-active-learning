# Representation quality versus query strategy in active learning for scanning-electron micrographs

Vishesh Srivastava · technical report accompanying the `microscopy-active-learning` repository

## Abstract

Active learning is often proposed to cut the cost of labelling microscopy images, but its benefit depends on the
representation it operates on and on how the data shifts between instruments, magnifications and samples. We
build a seeded framework that compares five query strategies (random, entropy, k-center diversity, a hybrid, and a
cost-aware variant) on frozen embeddings, under real and synthetic shifts, with specimen-grouped splits and
Holm-corrected paired tests over 10 seeds. On 961 real SEM micrographs of ultrahigh-carbon steel (UHCSDB), the
encoder explains almost all of the variation: frozen DINOv2 features raise in-distribution accuracy from 0.55–0.61
to 0.72–0.77 and detector-shift accuracy from the majority-class level (0.30–0.40) to 0.67–0.71, while no query
strategy beats random sampling. The same holds for classification and regression on the Aachen–Heerlen steel set
(1,705 images). Uncertainty is poorly calibrated under shift, and diversity-driven selection makes surrogate
intervals under-cover. We conclude that, at pool sizes of a few hundred images, effort is better spent on
representations and calibration than on acquisition heuristics.

## 1. Question

Given a pool of unlabeled micrographs and a small labelling budget, which images should be labelled first? We ask
three things: (i) does an acquisition strategy beat random selection, (ii) how much of the result is determined by
the encoder, and (iii) do conclusions survive real shifts in magnification, detector and sample.

## 2. Method

**Pipeline.** Images are embedded once by a frozen encoder. A pool-based loop starts from 8–14 random labels and adds
8–10 per round for 8 rounds. Classification uses a logistic-regression head with predictive entropy; regression uses a
Gaussian-process surrogate (PCA to 16 dimensions, RBF + white noise) with predictive standard deviation.

**Strategies.** Random; maximum uncertainty; greedy k-center on the embeddings; hybrid (top 4b most uncertain, then k-center
among them); cost-aware (uncertainty divided by an assumed acquisition cost).

**Encoders.** A three-block CNN, either randomly initialised or trained with SimCLR on the unlabeled pool; training-free
multi-scale texture features (intensity, gradient and LBP-style histograms); frozen DINOv2-small and -base. A CLIP-style
SEM+EBSD objective is evaluated on synthetic registered pairs.

**Statistics.** Per-seed area under the learning curve (ALC) is compared to random with a paired Wilcoxon test; we report
95% bootstrap intervals and Holm-adjusted p-values within each table.

## 3. Data and protocol

| Dataset | Content | Task | Splits and shifts |
|---|---|---|---|
| Synthetic generator | 4 texture classes, paired EBSD-like maps, hardness-like property | class, property | scale ×1.5; second "instrument" (contrast, noise, blur, offset) |
| UHCSDB (CC BY 3.0 US) | 961 SEM micrographs, 44 specimens | 7 microconstituents | grouped by specimen (images without an ID excluded); magnification shift; SE→BSE detector shift |
| Aachen–Heerlen (CC0) | 1,705 SEM images, 10 steel sample types | temperature (400/500 °C); MA-island area fraction from expert polygons | grouped by sample type; tilt shift; cut-direction shift |

All reported numbers come from the same code path and seeds; every table is regenerated from the saved CSVs.

## 4. Results

**UHCSDB, accuracy at 94 labels** (majority class 0.348 / 0.170 / 0.300):

| Encoder (random strategy) | In-distribution | Magnification shift | Detector shift |
|---|---|---|---|
| CNN, SimCLR on pool | 0.553±0.074 | 0.428±0.103 | 0.372±0.073 |
| CNN, random init | 0.563±0.072 | 0.354±0.084 | 0.401±0.164 |
| Handcrafted features (128 px) | 0.608±0.072 | 0.406±0.061 | 0.299±0.135 |
| DINOv2-small | 0.722±0.068 | 0.569±0.131 | 0.666±0.178 |
| DINOv2-base | 0.770±0.050 | 0.602±0.158 | 0.708±0.122 |

1. **Encoder over strategy.** Changing the encoder moves accuracy by up to 0.4 (detector shift); changing the strategy moves ALC
   by at most 0.07, and the only UHCSDB difference to random that survives Holm correction is a loss (k-center diversity
   under magnification shift with a random-init CNN, −0.073).
2. **Self-supervision at this scale does not help.** SimCLR on ~190 unlabeled images is no better than a random-init CNN or
   handcrafted features (in-distribution 0.553 vs 0.563 vs 0.555 at 64 px).
3. **Aachen–Heerlen.** MA-island area fraction is predicted with R² ≈ 0.34 in distribution and 0.39 under a cut-direction
   shift, but only ≈ 0.10 under tilt; RMSE 0.057 against 0.077 for the mean predictor. Transformation temperature of
   unseen steel types is at the majority-class rate (0.49 vs 0.44). No strategy improves on random.
4. **Calibration.** On the synthetic instrument shift the head is 95% confident at 25% accuracy (ECE 0.70). GP 90% intervals cover
   0.88 in distribution and 0.66–0.71 under shift; on Aachen–Heerlen, diversity and hybrid selection reduce coverage from 0.87 to
   0.75–0.76 (Holm p = 0.02).
5. **Synthetic results do not transfer.** Per-image normalisation plus strong augmentation lifted synthetic instrument-shift
   accuracy from chance to 0.37 and degraded UHCSDB detector-shift accuracy to 0.18–0.23.
6. **Cross-modal pretraining.** On synthetic SEM+EBSD pairs, a CLIP-style encoder gave the best property R² (0.74 at 48 labels vs
   0.64 for SimCLR and 0.70 random-init); 5 seeds, no significance test.

## 5. Discussion

With a few hundred candidates and a budget of under a hundred labels, random sampling already covers the data
well; uncertainty- and diversity-based selection concentrate on atypical points, which neither helps a linear head nor
a GP fit and can hurt calibration. Strong representations change the problem far more than selection does. The
poor behaviour of uncertainty under shift suggests that useful acquisition needs shift-aware, calibrated uncertainty
(ensembles, conformal prediction) rather than raw entropy.

## 6. Limitations

Small pools and crops, frozen encoders, one real SEM collection with image-level labels, no measured mechanical
properties, and a synthetic EBSD that is a deterministic function of the same grains. Cost models are assumptions. UHCSDB
is read from a Zenodo-archived mirror (hash-verified against its own manifest). The Aachen–Heerlen images are
embedded on a GPU; only the embeddings are kept.

## 7. Reproducibility

Code, tests and CI: <https://github.com/iamvisheshsrivastava/microscopy-active-learning>. Seeds are fixed; each result
is a CSV in `results/`; `scripts/resummarize.py` regenerates all tables; `scripts/get_uhcsdb.py` and
`scripts/kaggle_submit.py` fetch data and run GPU jobs. Datasets are not redistributed.

## References

- DeCost et al., UHCSDB, *Integr. Mater. Manuf. Innov.* 6, 197–205 (2017).
- Iren et al., Aachen–Heerlen annotated steel microstructure dataset, *Sci. Data* (2021).
- Chen et al., SimCLR (2020); Radford et al., CLIP (2021); Oquab et al., DINOv2 (2023).
