Encoder: contrastive (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.553±0.074 (0.518) | 0.428±0.103 (0.379) | 0.372±0.073 (0.334) |
| uncertainty | 0.545±0.052 (0.507) | 0.397±0.083 (0.336) | 0.343±0.091 (0.342) |
| diversity | 0.568±0.078 (0.524) | 0.381±0.061 (0.316) | 0.324±0.085 (0.302) |
| hybrid | 0.546±0.054 (0.530) | 0.375±0.074 (0.346) | 0.306±0.131 (0.319) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.011 (p=0.38) | -0.042 (p=0.70) | +0.008 (p=0.62) |
| diversity | +0.006 (p=0.38) | -0.063 (p=0.11) | -0.032 (p=0.23) |
| hybrid | +0.012 (p=0.28) | -0.033 (p=0.38) | -0.015 (p=0.38) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.308±0.076 (0.288) | 0.219±0.083 (0.213) | 0.351±0.113 (0.305) |
| uncertainty | 0.301±0.060 (0.277) | 0.179±0.038 (0.167) | 0.334±0.128 (0.315) |
| diversity | 0.307±0.097 (0.282) | 0.200±0.098 (0.187) | 0.286±0.066 (0.280) |
| hybrid | 0.297±0.076 (0.287) | 0.201±0.099 (0.205) | 0.242±0.118 (0.276) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.011 (p=0.23) | -0.046 (p=0.13) | +0.009 (p=0.77) |
| diversity | -0.005 (p=0.70) | -0.026 (p=0.11) | -0.025 (p=0.70) |
| hybrid | -0.001 (p=0.77) | -0.008 (p=0.49) | -0.029 (p=0.49) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.186±0.066 (0.239) | 0.319±0.087 (0.396) | 0.361±0.102 (0.424) |
| uncertainty | 0.234±0.054 (0.302) | 0.393±0.113 (0.486) | 0.460±0.086 (0.479) |
| diversity | 0.163±0.063 (0.229) | 0.335±0.057 (0.414) | 0.406±0.100 (0.447) |
| hybrid | 0.217±0.061 (0.265) | 0.398±0.080 (0.454) | 0.414±0.095 (0.470) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.063 (p=0.00) | +0.090 (p=0.00) | +0.055 (p=0.05) |
| diversity | -0.010 (p=0.28) | +0.018 (p=0.77) | +0.023 (p=0.49) |
| hybrid | +0.026 (p=0.23) | +0.058 (p=0.04) | +0.047 (p=0.01) |