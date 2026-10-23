Encoder: classical (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.555±0.059 (0.539) | 0.366±0.087 (0.347) | 0.354±0.172 (0.334) |
| uncertainty | 0.558±0.063 (0.540) | 0.391±0.092 (0.352) | 0.283±0.098 (0.291) |
| diversity | 0.555±0.076 (0.529) | 0.366±0.070 (0.282) | 0.420±0.205 (0.390) |
| hybrid | 0.571±0.046 (0.534) | 0.418±0.092 (0.340) | 0.371±0.149 (0.341) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | +0.001 [-0.019, +0.022] p=0.77 (Holm 1.00) | +0.005 [-0.022, +0.028] p=0.56 (Holm 1.00) | -0.044 [-0.175, +0.070] p=0.56 (Holm 1.00) |
| diversity | -0.010 [-0.031, +0.010] p=0.43 (Holm 1.00) | -0.065 [-0.126, -0.015] p=0.06 (Holm 0.58) | +0.055 [-0.008, +0.119] p=0.23 (Holm 1.00) |
| hybrid | -0.005 [-0.025, +0.015] p=0.77 (Holm 1.00) | -0.007 [-0.067, +0.059] p=0.77 (Holm 1.00) | +0.006 [-0.095, +0.086] p=0.70 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.290±0.065 (0.284) | 0.191±0.041 (0.179) | 0.278±0.179 (0.263) |
| uncertainty | 0.301±0.064 (0.290) | 0.197±0.052 (0.192) | 0.223±0.089 (0.232) |
| diversity | 0.282±0.054 (0.268) | 0.169±0.050 (0.148) | 0.336±0.205 (0.310) |
| hybrid | 0.297±0.054 (0.281) | 0.181±0.051 (0.164) | 0.289±0.159 (0.269) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | +0.006 [-0.008, +0.021] p=0.70 (Holm 1.00) | +0.013 [-0.016, +0.037] p=0.13 (Holm 1.00) | -0.031 [-0.131, +0.055] p=1.00 (Holm 1.00) |
| diversity | -0.017 [-0.036, -0.001] p=0.16 (Holm 1.00) | -0.032 [-0.073, +0.003] p=0.32 (Holm 1.00) | +0.047 [+0.007, +0.091] p=0.19 (Holm 1.00) |
| hybrid | -0.003 [-0.015, +0.009] p=0.70 (Holm 1.00) | -0.016 [-0.065, +0.032] p=0.62 (Holm 1.00) | +0.006 [-0.062, +0.054] p=0.32 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.278±0.058 (0.277) | 0.463±0.064 (0.470) | 0.520±0.145 (0.531) |
| uncertainty | 0.285±0.063 (0.280) | 0.450±0.079 (0.473) | 0.612±0.129 (0.583) |
| diversity | 0.257±0.064 (0.265) | 0.437±0.059 (0.497) | 0.470±0.177 (0.459) |
| hybrid | 0.269±0.047 (0.286) | 0.429±0.062 (0.488) | 0.511±0.156 (0.523) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.003 [-0.011, +0.020] p=1.00 (Holm 1.00) | +0.003 [-0.020, +0.029] p=0.92 (Holm 1.00) | +0.052 [-0.055, +0.171] p=0.43 (Holm 1.00) |
| diversity | -0.012 [-0.037, +0.007] p=0.77 (Holm 1.00) | +0.027 [-0.020, +0.083] p=0.62 (Holm 1.00) | -0.071 [-0.141, -0.005] p=0.19 (Holm 1.00) |
| hybrid | +0.009 [-0.013, +0.035] p=0.70 (Holm 1.00) | +0.018 [-0.033, +0.066] p=0.62 (Holm 1.00) | -0.008 [-0.081, +0.074] p=0.62 (Holm 1.00) |
