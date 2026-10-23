Encoder: random (norm_input=True, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.549±0.056 (0.549) | 0.417±0.080 (0.391) | 0.226±0.152 (0.215) |
| uncertainty | 0.564±0.050 (0.537) | 0.455±0.081 (0.392) | 0.200±0.120 (0.209) |
| diversity | 0.582±0.051 (0.556) | 0.435±0.079 (0.411) | 0.220±0.127 (0.238) |
| hybrid | 0.579±0.057 (0.550) | 0.446±0.086 (0.378) | 0.199±0.085 (0.215) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.013 [-0.033, +0.010] p=0.16 (Holm 1.00) | +0.001 [-0.044, +0.046] p=1.00 (Holm 1.00) | -0.007 [-0.047, +0.038] p=0.62 (Holm 1.00) |
| diversity | +0.007 [-0.014, +0.028] p=0.49 (Holm 1.00) | +0.020 [-0.029, +0.082] p=0.85 (Holm 1.00) | +0.023 [-0.035, +0.073] p=0.32 (Holm 1.00) |
| hybrid | +0.000 [-0.015, +0.016] p=1.00 (Holm 1.00) | -0.013 [-0.075, +0.053] p=0.56 (Holm 1.00) | -0.001 [-0.048, +0.048] p=0.85 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.302±0.049 (0.289) | 0.225±0.063 (0.200) | 0.189±0.161 (0.188) |
| uncertainty | 0.301±0.069 (0.287) | 0.202±0.041 (0.207) | 0.203±0.130 (0.202) |
| diversity | 0.298±0.057 (0.289) | 0.212±0.066 (0.188) | 0.169±0.113 (0.189) |
| hybrid | 0.288±0.042 (0.286) | 0.193±0.053 (0.177) | 0.166±0.070 (0.188) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.003 [-0.019, +0.015] p=0.62 (Holm 1.00) | +0.007 [-0.015, +0.031] p=0.77 (Holm 1.00) | +0.014 [-0.028, +0.054] p=0.56 (Holm 1.00) |
| diversity | +0.000 [-0.013, +0.014] p=0.85 (Holm 1.00) | -0.012 [-0.027, +0.008] p=0.08 (Holm 0.67) | +0.001 [-0.091, +0.060] p=0.28 (Holm 1.00) |
| hybrid | -0.003 [-0.017, +0.011] p=0.85 (Holm 1.00) | -0.023 [-0.044, -0.005] p=0.05 (Holm 0.44) | -0.000 [-0.057, +0.051] p=0.85 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.265±0.061 (0.261) | 0.392±0.068 (0.428) | 0.598±0.131 (0.595) |
| uncertainty | 0.278±0.045 (0.297) | 0.407±0.083 (0.458) | 0.656±0.134 (0.626) |
| diversity | 0.226±0.057 (0.233) | 0.368±0.079 (0.383) | 0.591±0.173 (0.560) |
| hybrid | 0.249±0.073 (0.273) | 0.400±0.073 (0.461) | 0.635±0.107 (0.618) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.037 [+0.024, +0.051] p=0.00 (Holm 0.02) | +0.031 [+0.005, +0.055] p=0.08 (Holm 0.42) | +0.031 [-0.028, +0.083] p=0.43 (Holm 0.86) |
| diversity | -0.028 [-0.042, -0.013] p=0.01 (Holm 0.08) | -0.045 [-0.085, -0.014] p=0.01 (Holm 0.10) | -0.034 [-0.089, +0.033] p=0.19 (Holm 0.58) |
| hybrid | +0.012 [-0.005, +0.027] p=0.13 (Holm 0.52) | +0.033 [-0.001, +0.071] p=0.05 (Holm 0.29) | +0.024 [-0.026, +0.072] p=0.43 (Holm 0.86) |
