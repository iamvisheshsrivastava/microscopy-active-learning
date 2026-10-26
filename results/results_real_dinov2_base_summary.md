Encoder: pretrained (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.770±0.050 (0.741) | 0.602±0.158 (0.534) | 0.708±0.122 (0.645) |
| uncertainty | 0.755±0.064 (0.720) | 0.621±0.119 (0.543) | 0.697±0.108 (0.619) |
| diversity | 0.774±0.045 (0.744) | 0.603±0.134 (0.578) | 0.703±0.120 (0.687) |
| hybrid | 0.772±0.059 (0.746) | 0.641±0.147 (0.588) | 0.737±0.140 (0.683) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.022 [-0.046, -0.002] p=0.16 (Holm 1.00) | +0.008 [-0.064, +0.071] p=0.49 (Holm 1.00) | -0.027 [-0.093, +0.026] p=0.62 (Holm 1.00) |
| diversity | +0.003 [-0.010, +0.018] p=1.00 (Holm 1.00) | +0.044 [+0.009, +0.088] p=0.04 (Holm 0.30) | +0.041 [-0.010, +0.115] p=0.43 (Holm 1.00) |
| hybrid | +0.005 [-0.012, +0.029] p=0.85 (Holm 1.00) | +0.053 [+0.013, +0.100] p=0.03 (Holm 0.25) | +0.038 [-0.018, +0.114] p=0.49 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.467±0.156 (0.424) | 0.372±0.118 (0.300) | 0.597±0.217 (0.551) |
| uncertainty | 0.449±0.168 (0.414) | 0.398±0.094 (0.352) | 0.594±0.196 (0.527) |
| diversity | 0.506±0.178 (0.441) | 0.373±0.137 (0.341) | 0.590±0.220 (0.586) |
| hybrid | 0.473±0.161 (0.437) | 0.372±0.091 (0.344) | 0.617±0.232 (0.581) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.010 [-0.027, +0.009] p=0.32 (Holm 1.00) | +0.051 [+0.011, +0.097] p=0.11 (Holm 0.95) | -0.024 [-0.066, +0.015] p=0.32 (Holm 1.00) |
| diversity | +0.017 [-0.016, +0.059] p=0.85 (Holm 1.00) | +0.040 [+0.002, +0.080] p=0.13 (Holm 1.00) | +0.035 [-0.006, +0.094] p=0.43 (Holm 1.00) |
| hybrid | +0.013 [-0.010, +0.038] p=0.49 (Holm 1.00) | +0.043 [+0.002, +0.089] p=0.13 (Holm 1.00) | +0.030 [-0.011, +0.088] p=0.32 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.151±0.032 (0.156) | 0.257±0.119 (0.289) | 0.192±0.071 (0.233) |
| uncertainty | 0.168±0.051 (0.171) | 0.256±0.110 (0.300) | 0.199±0.059 (0.246) |
| diversity | 0.146±0.030 (0.144) | 0.247±0.113 (0.254) | 0.175±0.078 (0.189) |
| hybrid | 0.156±0.040 (0.151) | 0.241±0.108 (0.252) | 0.158±0.068 (0.194) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.015 [-0.002, +0.033] p=0.19 (Holm 1.00) | +0.012 [-0.029, +0.056] p=0.77 (Holm 1.00) | +0.012 [-0.030, +0.063] p=0.77 (Holm 1.00) |
| diversity | -0.012 [-0.032, +0.003] p=0.92 (Holm 1.00) | -0.035 [-0.067, -0.005] p=0.11 (Holm 0.74) | -0.045 [-0.102, -0.010] p=0.01 (Holm 0.09) |
| hybrid | -0.004 [-0.028, +0.013] p=0.77 (Holm 1.00) | -0.036 [-0.068, -0.008] p=0.08 (Holm 0.67) | -0.040 [-0.100, +0.002] p=0.19 (Holm 1.00) |
