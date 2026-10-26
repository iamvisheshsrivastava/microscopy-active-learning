# microscopy-active-learning

[![ci](https://github.com/iamvisheshsrivastava/microscopy-active-learning/actions/workflows/ci.yml/badge.svg)](https://github.com/iamvisheshsrivastava/microscopy-active-learning/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A framework for studying **representation learning and active learning on multi-scale scientific imaging data**. It
combines self-supervised and cross-modal (SEM + EBSD) embeddings, pool-based acquisition under cost and uncertainty,
and property surrogates, and evaluates all of them under scale, instrument and acquisition shift. Everything is seeded,
tested, and reproducible from the command line, on a controllable synthetic generator and on two real steel
micrograph collections.

[Results page](https://iamvisheshsrivastava.github.io/microscopy-active-learning/) ·
[Technical report](docs/report.md) ·
[Full results](docs/results.md)

## What the experiments show

1. **Representation quality dominates; the query strategy barely matters.** On UHCSDB (961 real SEM micrographs,
   7 microconstituents, specimen-grouped splits), frozen DINOv2 features lift in-distribution accuracy from 0.55–0.61 (small CNNs
   trained from scratch, handcrafted texture features) to 0.72–0.77, and detector-shift (SE→BSE) accuracy from the
   majority-class level (0.30–0.40) to 0.67–0.71.
2. **Active learning did not beat random sampling in any real-data setting** once p-values are corrected for multiple
   comparisons (10 seeds, Holm). That holds for classification on UHCSDB, and for classification and regression on
   the Aachen–Heerlen steel set. The differences that do survive correction are losses (for example k-center diversity
   under magnification shift, and reduced interval coverage on Aachen–Heerlen).
3. **Uncertainty estimates are not reliable under shift.** The classifier is ~95% confident while ~25% correct on a shifted
   synthetic instrument, and GP prediction intervals fall from 0.88 to 0.66–0.71 coverage (nominal 0.90) on shifted data.
4. **Synthetic benchmarks did not predict real behaviour.** A normalisation-plus-augmentation recipe that
   helped on the synthetic instrument shift made real detector shift worse.
5. **Pairing SEM with EBSD during pretraining improved a property surrogate** on the synthetic pairs (R² 0.74 vs 0.64
   for SEM-only SimCLR at 48 labels, 5 seeds, no significance test).

## What is in the repository

| Component | Where |
|---|---|
| Seeded synthetic microstructure generator (SEM, EBSD-like maps, property, cost) | `src/maldl/data/synthetic.py` |
| Real-data loaders (UHCSDB, generic metadata CSV), group-aware splits | `src/maldl/data/` |
| Encoders: small CNN, handcrafted features, frozen pretrained backbones (DINOv2) | `src/maldl/models/` |
| SimCLR-style and CLIP-style (SEM+EBSD) pretraining | `src/maldl/training/` |
| Query strategies (random, uncertainty, k-center diversity, hybrid, cost-aware), classification and GP-regression loops | `src/maldl/active/` |
| Calibration (ECE, interval coverage), paired Wilcoxon tests, Holm correction, bootstrap CIs | `src/maldl/eval/` |
| Experiment CLIs, Kaggle GPU job runner, dataset fetch/verify scripts | `scripts/` |
| 32 tests, CI | `tests/`, `.github/workflows/` |

## Quick start

```bash
pip install torch                      # CPU is enough for everything except the pretrained backbones
pip install -e ".[dev]"
pytest -q                              # 32 tests, under a minute

# synthetic benchmark
python scripts/run_experiment.py --tag _baseline
python scripts/run_surrogate_al.py
python scripts/run_multimodal.py

# real data
python scripts/get_uhcsdb.py                       # clone the UHCSDB mirror and verify SHA-256 hashes
python scripts/run_real.py --encoder classical --size 128 --tag _real_classical128
python scripts/kaggle_submit.py --job pretrained   # frozen DINOv2 on a free Kaggle GPU (needs a Kaggle token)
python scripts/kaggle_submit.py --job aachen       # embed the Aachen-Heerlen images on GPU
python scripts/run_aachen.py --task reg --backbone base

python scripts/resummarize.py                      # rebuild every summary table from the saved CSVs
```

Every run writes `results/<tag>.csv` (all seeds and rounds), a learning-curve `.png` and a `_summary.md`.
`results/README.md` maps each file to the command that produced it.

## Results at a glance

Accuracy at 94 labels on UHCSDB, mean ± std over 10 specimen-grouped splits. The majority-class baseline is 0.348 /
0.170 / 0.300. Shifts are real: magnification (SE detector, high magnification) and detector (BSE).

| Encoder | Strategy | In-distribution | Magnification shift | Detector shift |
|---|---|---|---|---|
| CNN, SimCLR on the pool | random | 0.553±0.074 | 0.428±0.103 | 0.372±0.073 |
| CNN, random init | random | 0.563±0.072 | 0.354±0.084 | 0.401±0.164 |
| Handcrafted features, 128 px | random | 0.608±0.072 | 0.406±0.061 | 0.299±0.135 |
| DINOv2-small, frozen | random | 0.722±0.068 | 0.569±0.131 | 0.666±0.178 |
| DINOv2-base, frozen | random | 0.770±0.050 | 0.602±0.158 | 0.708±0.122 |
| DINOv2-base, frozen | hybrid | 0.772±0.059 | 0.641±0.147 | 0.737±0.140 |

On the Aachen–Heerlen set (steel sample types held out), the MA-island area fraction is predicted with R² ≈ 0.34
(RMSE 0.057 vs 0.077 for the mean predictor); transformation temperature of unseen steels is not recoverable
(0.49 vs 0.44 majority). Details, all strategies, calibration and tests: [docs/results.md](docs/results.md).

## Method notes

- **Splits.** Real images are split by specimen or steel sample type, never by image. Images without a specimen ID
  (about 160 of UHCSDB) are excluded because they cannot be grouped safely.
- **Protocol.** Pool-based loop on frozen embeddings; logistic-regression head (classification) or Gaussian-process surrogate
  (regression); 8 acquisition rounds; strategies compared by area under the learning curve.
- **Statistics.** Paired Wilcoxon on per-seed ALC against random, 95% bootstrap CIs, Holm adjustment within each table.
  Claims in this repository quote the adjusted values.
- **Compute.** CPU for the small models; a free Kaggle T4 for pretrained backbones and the Aachen–Heerlen embeddings.

## Scope and limitations

- The synthetic benchmark is a controlled testbed with assumed property and cost models, and an EBSD map that is a
  deterministic function of the same grains. It is used to isolate effects, not to estimate real performance.
- Real-data studies use one SEM collection with image-level labels and one steel-sample collection. There are no real
  registered SEM/EBSD pairs and no measured mechanical properties yet.
- Images are small crops (64–224 px) of larger micrographs; pretrained backbones are evaluated frozen, not fine-tuned.
  Pool sizes are a few hundred images, so differences of a few points are within noise.
- UHCSDB is read from a hash-verified Zenodo-archived mirror because the original NIST host was unreachable.

## Roadmap

Open questions are tracked as [issues](https://github.com/iamvisheshsrivastava/microscopy-active-learning/issues):
fine-tuning and scale-aware encoders, calibrated and shift-aware acquisition (ensembles, conformal, BADGE/BALD),
measured acquisition costs, real SEM/EBSD pairs, and surrogates for measured properties.

## Data and citation

- **UHCSDB**: DeCost et al., *Integr. Mater. Manuf. Innov.* 6, 197–205 (2017), doi:10.1007/s40192-017-0097-0, CC BY 3.0 US;
  mirror doi:10.5281/zenodo.23050463.
- **Aachen–Heerlen annotated steel microstructure dataset**: Iren et al., *Sci. Data* (2021), doi:10.1038/s41597-021-00926-7, CC0.
- DINOv2: Oquab et al., 2023 (weights fetched from the Hugging Face hub at run time).

Datasets are never committed. To cite this software, see [`CITATION.cff`](CITATION.cff). Contributions are welcome;
see [`CONTRIBUTING.md`](CONTRIBUTING.md). MIT licensed.
