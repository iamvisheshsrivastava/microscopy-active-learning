## Property RMSE (HV-like units, lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_rmse | scale_shift_rmse | source_shift_rmse |
|---|---|---|---|
| random | 21.575±1.729 (24.185) | 34.370±2.481 (35.185) | 41.572±9.711 (39.022) |
| uncertainty | 21.266±1.375 (23.646) | 34.623±2.895 (34.918) | 39.330±5.144 (37.440) |
| diversity | 20.907±1.804 (23.103) | 35.214±2.103 (35.761) | 42.992±12.300 (39.241) |
| hybrid | 21.180±1.472 (23.466) | 35.306±2.522 (36.332) | 41.681±9.416 (38.339) |
| cost_uncertainty | 25.234±3.884 (27.122) | 43.332±2.188 (42.103) | 34.901±4.702 (35.609) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_rmse | scale_shift_rmse | source_shift_rmse |
|---|---|---|---|
| uncertainty | -0.539 (p=0.49) | -0.267 (p=0.85) | -1.582 (p=0.16) |
| diversity | -1.081 (p=0.23) | +0.576 (p=0.77) | +0.219 (p=0.92) |
| hybrid | -0.718 (p=0.62) | +1.147 (p=0.32) | -0.683 (p=0.70) |
| cost_uncertainty | +2.937 (p=0.05) | +6.919 (p=0.00) | -3.412 (p=0.16) |

## Property R2 (higher is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_r2 | scale_shift_r2 | source_shift_r2 |
|---|---|---|---|
| random | 0.700±0.047 (0.612) | 0.235±0.105 (0.195) | -0.172±0.609 (-0.017) |
| uncertainty | 0.709±0.037 (0.629) | 0.221±0.133 (0.204) | -0.014±0.286 (0.081) |
| diversity | 0.717±0.048 (0.647) | 0.198±0.092 (0.167) | -0.288±0.824 (-0.041) |
| hybrid | 0.711±0.041 (0.637) | 0.192±0.116 (0.139) | -0.176±0.614 (0.017) |
| cost_uncertainty | 0.582±0.132 (0.497) | -0.214±0.125 (-0.160) | 0.201±0.239 (0.158) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_r2 | scale_shift_r2 | source_shift_r2 |
|---|---|---|---|
| uncertainty | +0.017 (p=0.49) | +0.010 (p=0.92) | +0.098 (p=0.11) |
| diversity | +0.035 (p=0.28) | -0.028 (p=0.85) | -0.024 (p=0.77) |
| hybrid | +0.025 (p=0.56) | -0.056 (p=0.32) | +0.034 (p=0.70) |
| cost_uncertainty | -0.115 (p=0.05) | -0.355 (p=0.00) | +0.175 (p=0.13) |

## 90% interval coverage (nominal 0.90)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_cov90 | scale_shift_cov90 | source_shift_cov90 |
|---|---|---|---|
| random | 0.885±0.030 (0.854) | 0.680±0.084 (0.707) | 0.691±0.105 (0.750) |
| uncertainty | 0.865±0.051 (0.853) | 0.629±0.102 (0.663) | 0.708±0.041 (0.748) |
| diversity | 0.887±0.030 (0.857) | 0.635±0.088 (0.655) | 0.659±0.168 (0.724) |
| hybrid | 0.874±0.036 (0.836) | 0.616±0.091 (0.630) | 0.657±0.137 (0.725) |
| cost_uncertainty | 0.825±0.066 (0.816) | 0.491±0.046 (0.555) | 0.785±0.052 (0.799) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_cov90 | scale_shift_cov90 | source_shift_cov90 |
|---|---|---|---|
| uncertainty | -0.001 (p=0.92) | -0.044 (p=0.13) | -0.002 (p=0.92) |
| diversity | +0.003 (p=0.92) | -0.052 (p=0.28) | -0.026 (p=0.56) |
| hybrid | -0.019 (p=0.43) | -0.077 (p=0.06) | -0.025 (p=0.51) |
| cost_uncertainty | -0.039 (p=0.23) | -0.152 (p=0.00) | +0.049 (p=0.03) |