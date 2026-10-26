DINOv2-base; task=cls; grouped by steel sample type; mean sizes: in_dist=248, tilt_shift=74, direction_shift=216, pool=444
Majority-class accuracy: in_dist=0.441, tilt_shift=0.430, direction_shift=0.353

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | tilt_shift | direction_shift |
|---|---|---|---|
| random | 0.494±0.102 (0.483) | 0.589±0.150 (0.571) | 0.465±0.118 (0.434) |
| uncertainty | 0.497±0.096 (0.476) | 0.533±0.064 (0.525) | 0.463±0.127 (0.419) |
| diversity | 0.497±0.076 (0.486) | 0.528±0.107 (0.503) | 0.445±0.098 (0.412) |
| hybrid | 0.489±0.107 (0.485) | 0.523±0.069 (0.503) | 0.412±0.082 (0.407) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | tilt_shift | direction_shift |
|---|---|---|---|
| uncertainty | -0.007 [-0.034, +0.024] p=0.62 (Holm 1.00) | -0.046 [-0.112, +0.016] p=0.32 (Holm 1.00) | -0.015 [-0.065, +0.040] p=0.56 (Holm 1.00) |
| diversity | +0.003 [-0.033, +0.037] p=0.92 (Holm 1.00) | -0.068 [-0.167, +0.001] p=0.13 (Holm 1.00) | -0.022 [-0.053, +0.009] p=0.23 (Holm 1.00) |
| hybrid | +0.002 [-0.033, +0.034] p=0.92 (Holm 1.00) | -0.067 [-0.163, +0.014] p=0.23 (Holm 1.00) | -0.027 [-0.059, +0.004] p=0.16 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | tilt_shift_bacc | direction_shift_bacc |
|---|---|---|---|
| random | 0.521±0.097 (0.519) | 0.577±0.135 (0.560) | 0.501±0.118 (0.483) |
| uncertainty | 0.524±0.076 (0.519) | 0.535±0.043 (0.537) | 0.529±0.124 (0.492) |
| diversity | 0.513±0.084 (0.515) | 0.546±0.073 (0.532) | 0.502±0.114 (0.479) |
| hybrid | 0.513±0.067 (0.513) | 0.543±0.050 (0.533) | 0.485±0.089 (0.482) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | tilt_shift_bacc | direction_shift_bacc |
|---|---|---|---|
| uncertainty | +0.000 [-0.036, +0.039] p=0.92 (Holm 1.00) | -0.023 [-0.082, +0.035] p=0.92 (Holm 1.00) | +0.009 [-0.045, +0.063] p=0.85 (Holm 1.00) |
| diversity | -0.004 [-0.045, +0.039] p=0.77 (Holm 1.00) | -0.028 [-0.060, +0.006] p=0.19 (Holm 1.00) | -0.004 [-0.045, +0.040] p=0.92 (Holm 1.00) |
| hybrid | -0.006 [-0.043, +0.031] p=0.70 (Holm 1.00) | -0.027 [-0.079, +0.024] p=0.49 (Holm 1.00) | -0.001 [-0.042, +0.041] p=0.77 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | tilt_shift_ece | direction_shift_ece |
|---|---|---|---|
| random | 0.400±0.117 (0.409) | 0.335±0.153 (0.358) | 0.433±0.113 (0.458) |
| uncertainty | 0.408±0.109 (0.438) | 0.423±0.066 (0.422) | 0.452±0.133 (0.503) |
| diversity | 0.384±0.091 (0.404) | 0.432±0.131 (0.442) | 0.440±0.111 (0.477) |
| hybrid | 0.436±0.118 (0.435) | 0.460±0.081 (0.455) | 0.508±0.104 (0.514) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | tilt_shift_ece | direction_shift_ece |
|---|---|---|---|
| uncertainty | +0.029 [+0.001, +0.056] p=0.08 (Holm 0.50) | +0.064 [+0.006, +0.128] p=0.16 (Holm 0.65) | +0.046 [-0.010, +0.098] p=0.13 (Holm 0.65) |
| diversity | -0.005 [-0.046, +0.035] p=0.77 (Holm 1.00) | +0.084 [+0.013, +0.183] p=0.05 (Holm 0.44) | +0.019 [-0.016, +0.055] p=0.43 (Holm 1.00) |
| hybrid | +0.026 [-0.015, +0.070] p=0.49 (Holm 1.00) | +0.097 [+0.020, +0.188] p=0.05 (Holm 0.44) | +0.056 [+0.017, +0.095] p=0.05 (Holm 0.44) |
