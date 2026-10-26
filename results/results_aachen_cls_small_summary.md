DINOv2-small; task=cls; grouped by steel sample type; mean sizes: in_dist=248, tilt_shift=74, direction_shift=216, pool=444
Majority-class accuracy: in_dist=0.441, tilt_shift=0.430, direction_shift=0.353

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | tilt_shift | direction_shift |
|---|---|---|---|
| random | 0.466±0.071 (0.465) | 0.517±0.162 (0.512) | 0.457±0.131 (0.432) |
| uncertainty | 0.487±0.106 (0.477) | 0.523±0.159 (0.506) | 0.440±0.130 (0.428) |
| diversity | 0.471±0.089 (0.480) | 0.559±0.172 (0.526) | 0.458±0.181 (0.448) |
| hybrid | 0.470±0.112 (0.468) | 0.544±0.170 (0.515) | 0.409±0.170 (0.409) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | tilt_shift | direction_shift |
|---|---|---|---|
| uncertainty | +0.012 [-0.031, +0.049] p=0.38 (Holm 1.00) | -0.006 [-0.048, +0.034] p=0.77 (Holm 1.00) | -0.005 [-0.037, +0.037] p=0.32 (Holm 1.00) |
| diversity | +0.015 [-0.025, +0.054] p=0.56 (Holm 1.00) | +0.014 [-0.008, +0.037] p=0.32 (Holm 1.00) | +0.016 [-0.050, +0.087] p=0.85 (Holm 1.00) |
| hybrid | +0.003 [-0.040, +0.047] p=1.00 (Holm 1.00) | +0.003 [-0.044, +0.054] p=0.92 (Holm 1.00) | -0.024 [-0.077, +0.050] p=0.11 (Holm 0.95) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | tilt_shift_bacc | direction_shift_bacc |
|---|---|---|---|
| random | 0.491±0.071 (0.501) | 0.553±0.102 (0.543) | 0.501±0.131 (0.488) |
| uncertainty | 0.523±0.075 (0.514) | 0.549±0.132 (0.544) | 0.504±0.120 (0.492) |
| diversity | 0.495±0.100 (0.508) | 0.593±0.143 (0.564) | 0.526±0.171 (0.515) |
| hybrid | 0.506±0.089 (0.508) | 0.580±0.139 (0.557) | 0.489±0.167 (0.491) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | tilt_shift_bacc | direction_shift_bacc |
|---|---|---|---|
| uncertainty | +0.013 [-0.011, +0.043] p=0.62 (Holm 1.00) | +0.001 [-0.029, +0.037] p=0.85 (Holm 1.00) | +0.004 [-0.030, +0.045] p=0.70 (Holm 1.00) |
| diversity | +0.007 [-0.041, +0.057] p=0.92 (Holm 1.00) | +0.021 [-0.000, +0.042] p=0.23 (Holm 1.00) | +0.026 [-0.037, +0.093] p=0.70 (Holm 1.00) |
| hybrid | +0.007 [-0.024, +0.048] p=0.77 (Holm 1.00) | +0.014 [-0.025, +0.063] p=1.00 (Holm 1.00) | +0.002 [-0.051, +0.065] p=0.77 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | tilt_shift_ece | direction_shift_ece |
|---|---|---|---|
| random | 0.420±0.080 (0.415) | 0.440±0.164 (0.423) | 0.443±0.137 (0.455) |
| uncertainty | 0.441±0.123 (0.447) | 0.443±0.160 (0.454) | 0.498±0.149 (0.497) |
| diversity | 0.424±0.098 (0.408) | 0.417±0.161 (0.434) | 0.452±0.190 (0.454) |
| hybrid | 0.472±0.114 (0.458) | 0.436±0.187 (0.454) | 0.537±0.174 (0.524) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | tilt_shift_ece | direction_shift_ece |
|---|---|---|---|
| uncertainty | +0.032 [-0.013, +0.092] p=0.23 (Holm 1.00) | +0.031 [-0.021, +0.091] p=0.19 (Holm 1.00) | +0.042 [-0.009, +0.091] p=0.13 (Holm 1.00) |
| diversity | -0.007 [-0.047, +0.036] p=0.85 (Holm 1.00) | +0.011 [-0.010, +0.035] p=0.49 (Holm 1.00) | -0.001 [-0.071, +0.065] p=1.00 (Holm 1.00) |
| hybrid | +0.043 [+0.001, +0.098] p=0.13 (Holm 1.00) | +0.032 [-0.028, +0.093] p=0.13 (Holm 1.00) | +0.069 [-0.006, +0.126] p=0.08 (Holm 0.76) |
