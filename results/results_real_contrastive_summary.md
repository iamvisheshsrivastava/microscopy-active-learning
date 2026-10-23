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

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.011 [-0.025, +0.001] p=0.38 (Holm 1.00) | -0.042 [-0.108, +0.012] p=0.70 (Holm 1.00) | +0.008 [-0.032, +0.045] p=0.62 (Holm 1.00) |
| diversity | +0.006 [-0.022, +0.027] p=0.38 (Holm 1.00) | -0.063 [-0.122, -0.011] p=0.11 (Holm 0.95) | -0.032 [-0.073, +0.007] p=0.23 (Holm 1.00) |
| hybrid | +0.012 [-0.005, +0.029] p=0.28 (Holm 1.00) | -0.033 [-0.071, +0.004] p=0.38 (Holm 1.00) | -0.015 [-0.050, +0.023] p=0.38 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.308±0.076 (0.288) | 0.219±0.083 (0.213) | 0.351±0.113 (0.305) |
| uncertainty | 0.301±0.060 (0.277) | 0.179±0.038 (0.167) | 0.334±0.128 (0.315) |
| diversity | 0.307±0.097 (0.282) | 0.200±0.098 (0.187) | 0.286±0.066 (0.280) |
| hybrid | 0.297±0.076 (0.287) | 0.201±0.099 (0.205) | 0.242±0.118 (0.276) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.011 [-0.027, +0.003] p=0.23 (Holm 1.00) | -0.046 [-0.102, -0.007] p=0.13 (Holm 1.00) | +0.009 [-0.045, +0.083] p=0.77 (Holm 1.00) |
| diversity | -0.005 [-0.025, +0.014] p=0.70 (Holm 1.00) | -0.026 [-0.053, -0.002] p=0.11 (Holm 0.95) | -0.025 [-0.088, +0.040] p=0.70 (Holm 1.00) |
| hybrid | -0.001 [-0.019, +0.016] p=0.77 (Holm 1.00) | -0.008 [-0.024, +0.007] p=0.49 (Holm 1.00) | -0.029 [-0.080, +0.015] p=0.49 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.186±0.066 (0.239) | 0.319±0.087 (0.396) | 0.361±0.102 (0.424) |
| uncertainty | 0.234±0.054 (0.302) | 0.393±0.113 (0.486) | 0.460±0.086 (0.479) |
| diversity | 0.163±0.063 (0.229) | 0.335±0.057 (0.414) | 0.406±0.100 (0.447) |
| hybrid | 0.217±0.061 (0.265) | 0.398±0.080 (0.454) | 0.414±0.095 (0.470) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.063 [+0.038, +0.086] p=0.00 (Holm 0.04) | +0.090 [+0.035, +0.154] p=0.00 (Holm 0.04) | +0.055 [+0.016, +0.101] p=0.05 (Holm 0.24) |
| diversity | -0.010 [-0.029, +0.016] p=0.28 (Holm 0.93) | +0.018 [-0.041, +0.082] p=0.77 (Holm 0.98) | +0.023 [-0.015, +0.061] p=0.49 (Holm 0.98) |
| hybrid | +0.026 [-0.003, +0.058] p=0.23 (Holm 0.93) | +0.058 [+0.017, +0.096] p=0.04 (Holm 0.22) | +0.047 [+0.018, +0.079] p=0.01 (Holm 0.10) |
