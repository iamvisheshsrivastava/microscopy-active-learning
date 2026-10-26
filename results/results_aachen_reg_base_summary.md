DINOv2-base; task=reg; grouped by steel sample type; mean sizes: in_dist=248, tilt_shift=74, direction_shift=215, pool=444
Baseline RMSE (predict pool mean): in_dist=0.077, tilt_shift=0.074, direction_shift=0.075

## Property RMSE (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | direction_shift_rmse | in_dist_rmse | tilt_shift_rmse |
|---|---|---|---|
| random | 0.055±0.014 (0.059) | 0.057±0.013 (0.062) | 0.065±0.017 (0.069) |
| uncertainty | 0.060±0.015 (0.062) | 0.060±0.015 (0.064) | 0.068±0.017 (0.070) |
| diversity | 0.057±0.015 (0.061) | 0.058±0.014 (0.062) | 0.067±0.016 (0.068) |
| hybrid | 0.058±0.016 (0.061) | 0.058±0.014 (0.062) | 0.067±0.015 (0.068) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | direction_shift_rmse | in_dist_rmse | tilt_shift_rmse |
|---|---|---|---|
| uncertainty | +0.003 [+0.001, +0.005] p=0.05 (Holm 0.44) | +0.002 [+0.000, +0.004] p=0.11 (Holm 0.84) | +0.001 [-0.007, +0.007] p=0.32 (Holm 1.00) |
| diversity | +0.001 [-0.000, +0.002] p=0.11 (Holm 0.84) | +0.001 [-0.001, +0.002] p=0.62 (Holm 1.00) | -0.001 [-0.009, +0.004] p=0.32 (Holm 1.00) |
| hybrid | +0.001 [-0.000, +0.003] p=0.19 (Holm 1.00) | +0.001 [-0.001, +0.002] p=0.23 (Holm 1.00) | -0.001 [-0.009, +0.005] p=0.38 (Holm 1.00) |

## Property R2 (higher is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | direction_shift_r2 | in_dist_r2 | tilt_shift_r2 |
|---|---|---|---|
| random | 0.390±0.100 (0.267) | 0.343±0.137 (0.213) | 0.099±0.261 (-0.014) |
| uncertainty | 0.264±0.178 (0.186) | 0.284±0.180 (0.142) | 0.019±0.280 (-0.048) |
| diversity | 0.325±0.147 (0.236) | 0.324±0.180 (0.187) | 0.052±0.224 (0.036) |
| hybrid | 0.310±0.166 (0.232) | 0.324±0.179 (0.187) | 0.059±0.192 (0.029) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | direction_shift_r2 | in_dist_r2 | tilt_shift_r2 |
|---|---|---|---|
| uncertainty | -0.082 [-0.136, -0.030] p=0.05 (Holm 0.44) | -0.071 [-0.130, -0.014] p=0.11 (Holm 0.74) | -0.033 [-0.245, +0.223] p=0.38 (Holm 1.00) |
| diversity | -0.031 [-0.060, -0.003] p=0.11 (Holm 0.74) | -0.026 [-0.072, +0.017] p=0.49 (Holm 1.00) | +0.050 [-0.103, +0.276] p=0.49 (Holm 1.00) |
| hybrid | -0.035 [-0.072, +0.002] p=0.06 (Holm 0.52) | -0.026 [-0.061, +0.010] p=0.23 (Holm 1.00) | +0.043 [-0.121, +0.275] p=0.56 (Holm 1.00) |

## 90% interval coverage (nominal 0.90)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | direction_shift_cov90 | in_dist_cov90 | tilt_shift_cov90 |
|---|---|---|---|
| random | 0.891±0.085 (0.860) | 0.867±0.098 (0.839) | 0.853±0.162 (0.837) |
| uncertainty | 0.821±0.148 (0.832) | 0.809±0.149 (0.817) | 0.734±0.147 (0.782) |
| diversity | 0.779±0.168 (0.799) | 0.760±0.157 (0.777) | 0.691±0.126 (0.738) |
| hybrid | 0.758±0.199 (0.806) | 0.753±0.185 (0.786) | 0.706±0.114 (0.768) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | direction_shift_cov90 | in_dist_cov90 | tilt_shift_cov90 |
|---|---|---|---|
| uncertainty | -0.028 [-0.064, +0.012] p=0.23 (Holm 0.58) | -0.022 [-0.059, +0.021] p=0.23 (Holm 0.58) | -0.054 [-0.140, +0.042] p=0.19 (Holm 0.58) |
| diversity | -0.061 [-0.092, -0.035] p=0.00 (Holm 0.02) | -0.062 [-0.092, -0.039] p=0.00 (Holm 0.02) | -0.099 [-0.164, -0.017] p=0.08 (Holm 0.42) |
| hybrid | -0.054 [-0.089, -0.027] p=0.00 (Holm 0.02) | -0.053 [-0.088, -0.029] p=0.00 (Holm 0.02) | -0.068 [-0.128, +0.010] p=0.08 (Holm 0.42) |
