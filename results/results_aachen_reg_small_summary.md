DINOv2-small; task=reg; grouped by steel sample type; mean sizes: in_dist=248, tilt_shift=74, direction_shift=215, pool=444
Baseline RMSE (predict pool mean): in_dist=0.077, tilt_shift=0.074, direction_shift=0.075

## Property RMSE (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | direction_shift_rmse | in_dist_rmse | tilt_shift_rmse |
|---|---|---|---|
| random | 0.056±0.014 (0.061) | 0.058±0.013 (0.062) | 0.065±0.016 (0.068) |
| uncertainty | 0.057±0.014 (0.061) | 0.060±0.012 (0.064) | 0.068±0.014 (0.070) |
| diversity | 0.057±0.014 (0.061) | 0.062±0.012 (0.065) | 0.069±0.013 (0.070) |
| hybrid | 0.057±0.015 (0.060) | 0.059±0.013 (0.064) | 0.069±0.013 (0.070) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | direction_shift_rmse | in_dist_rmse | tilt_shift_rmse |
|---|---|---|---|
| uncertainty | +0.000 [-0.002, +0.003] p=0.77 (Holm 1.00) | +0.002 [-0.000, +0.005] p=0.19 (Holm 1.00) | +0.002 [-0.004, +0.009] p=0.70 (Holm 1.00) |
| diversity | -0.000 [-0.002, +0.002] p=0.70 (Holm 1.00) | +0.003 [-0.001, +0.008] p=0.32 (Holm 1.00) | +0.002 [-0.003, +0.007] p=0.49 (Holm 1.00) |
| hybrid | -0.000 [-0.003, +0.002] p=0.49 (Holm 1.00) | +0.002 [-0.001, +0.006] p=0.49 (Holm 1.00) | +0.002 [-0.003, +0.007] p=0.56 (Holm 1.00) |

## Property R2 (higher is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | direction_shift_r2 | in_dist_r2 | tilt_shift_r2 |
|---|---|---|---|
| random | 0.365±0.100 (0.231) | 0.321±0.142 (0.194) | 0.116±0.184 (0.022) |
| uncertainty | 0.322±0.149 (0.211) | 0.237±0.249 (0.124) | -0.033±0.413 (-0.088) |
| diversity | 0.330±0.135 (0.229) | 0.196±0.286 (0.102) | -0.080±0.402 (-0.064) |
| hybrid | 0.342±0.134 (0.242) | 0.268±0.204 (0.114) | -0.083±0.399 (-0.070) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | direction_shift_r2 | in_dist_r2 | tilt_shift_r2 |
|---|---|---|---|
| uncertainty | -0.020 [-0.096, +0.057] p=0.62 (Holm 1.00) | -0.070 [-0.141, +0.005] p=0.13 (Holm 1.00) | -0.110 [-0.352, +0.090] p=0.62 (Holm 1.00) |
| diversity | -0.001 [-0.079, +0.063] p=0.77 (Holm 1.00) | -0.092 [-0.282, +0.031] p=0.28 (Holm 1.00) | -0.086 [-0.260, +0.065] p=0.38 (Holm 1.00) |
| hybrid | +0.011 [-0.066, +0.079] p=0.49 (Holm 1.00) | -0.080 [-0.214, +0.011] p=0.43 (Holm 1.00) | -0.092 [-0.253, +0.054] p=0.32 (Holm 1.00) |

## 90% interval coverage (nominal 0.90)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | direction_shift_cov90 | in_dist_cov90 | tilt_shift_cov90 |
|---|---|---|---|
| random | 0.879±0.108 (0.852) | 0.856±0.113 (0.832) | 0.861±0.118 (0.857) |
| uncertainty | 0.889±0.071 (0.863) | 0.863±0.085 (0.836) | 0.826±0.088 (0.829) |
| diversity | 0.811±0.116 (0.827) | 0.779±0.107 (0.800) | 0.730±0.157 (0.790) |
| hybrid | 0.868±0.097 (0.856) | 0.822±0.124 (0.814) | 0.778±0.137 (0.805) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | direction_shift_cov90 | in_dist_cov90 | tilt_shift_cov90 |
|---|---|---|---|
| uncertainty | +0.011 [-0.019, +0.040] p=0.62 (Holm 1.00) | +0.004 [-0.033, +0.045] p=1.00 (Holm 1.00) | -0.028 [-0.073, +0.013] p=0.38 (Holm 1.00) |
| diversity | -0.025 [-0.066, +0.012] p=0.70 (Holm 1.00) | -0.032 [-0.072, +0.007] p=0.19 (Holm 1.00) | -0.067 [-0.141, -0.001] p=0.28 (Holm 1.00) |
| hybrid | +0.004 [-0.027, +0.033] p=0.85 (Holm 1.00) | -0.018 [-0.052, +0.016] p=0.32 (Holm 1.00) | -0.052 [-0.120, +0.010] p=0.23 (Holm 1.00) |
