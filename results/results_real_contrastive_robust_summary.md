Encoder: contrastive (norm_input=True, strong_aug=True); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.528±0.068 (0.522) | 0.398±0.131 (0.360) | 0.180±0.087 (0.194) |
| uncertainty | 0.532±0.068 (0.506) | 0.411±0.100 (0.359) | 0.196±0.122 (0.240) |
| diversity | 0.549±0.070 (0.526) | 0.390±0.069 (0.351) | 0.189±0.091 (0.221) |
| hybrid | 0.551±0.070 (0.526) | 0.382±0.069 (0.321) | 0.178±0.089 (0.207) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.017 [-0.043, +0.007] p=0.43 (Holm 1.00) | -0.001 [-0.041, +0.039] p=0.92 (Holm 1.00) | +0.045 [-0.000, +0.088] p=0.11 (Holm 0.95) |
| diversity | +0.004 [-0.015, +0.024] p=0.85 (Holm 1.00) | -0.009 [-0.057, +0.031] p=0.92 (Holm 1.00) | +0.027 [-0.011, +0.068] p=0.28 (Holm 1.00) |
| hybrid | +0.004 [-0.012, +0.019] p=0.56 (Holm 1.00) | -0.039 [-0.091, +0.006] p=0.28 (Holm 1.00) | +0.012 [-0.025, +0.046] p=0.70 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.291±0.047 (0.285) | 0.211±0.061 (0.181) | 0.154±0.081 (0.177) |
| uncertainty | 0.283±0.059 (0.289) | 0.185±0.059 (0.185) | 0.157±0.080 (0.216) |
| diversity | 0.314±0.078 (0.278) | 0.155±0.029 (0.152) | 0.177±0.060 (0.210) |
| hybrid | 0.288±0.059 (0.275) | 0.155±0.034 (0.144) | 0.159±0.083 (0.176) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | +0.005 [-0.025, +0.040] p=0.70 (Holm 1.00) | +0.004 [-0.018, +0.028] p=0.92 (Holm 1.00) | +0.039 [-0.008, +0.087] p=0.16 (Holm 0.96) |
| diversity | -0.006 [-0.029, +0.014] p=0.70 (Holm 1.00) | -0.029 [-0.056, -0.005] p=0.06 (Holm 0.45) | +0.033 [+0.009, +0.058] p=0.05 (Holm 0.39) |
| hybrid | -0.009 [-0.026, +0.007] p=0.43 (Holm 1.00) | -0.037 [-0.063, -0.015] p=0.01 (Holm 0.05) | -0.000 [-0.039, +0.037] p=0.92 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.233±0.069 (0.266) | 0.353±0.108 (0.429) | 0.607±0.086 (0.616) |
| uncertainty | 0.263±0.065 (0.310) | 0.375±0.114 (0.453) | 0.623±0.118 (0.588) |
| diversity | 0.211±0.061 (0.244) | 0.319±0.091 (0.396) | 0.559±0.121 (0.551) |
| hybrid | 0.214±0.075 (0.271) | 0.386±0.084 (0.462) | 0.611±0.111 (0.603) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.044 [+0.018, +0.070] p=0.03 (Holm 0.25) | +0.025 [-0.024, +0.078] p=0.56 (Holm 1.00) | -0.028 [-0.076, +0.016] p=0.38 (Holm 1.00) |
| diversity | -0.022 [-0.049, +0.006] p=0.23 (Holm 1.00) | -0.032 [-0.075, +0.014] p=0.23 (Holm 1.00) | -0.065 [-0.128, -0.004] p=0.13 (Holm 1.00) |
| hybrid | +0.005 [-0.016, +0.026] p=0.85 (Holm 1.00) | +0.034 [-0.017, +0.088] p=0.38 (Holm 1.00) | -0.013 [-0.076, +0.042] p=0.77 (Holm 1.00) |
