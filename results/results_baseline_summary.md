## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| random | 0.888±0.046 (0.838) | 0.534±0.126 (0.544) | 0.249±0.005 (0.249) |
| uncertainty | 0.934±0.041 (0.844) | 0.510±0.116 (0.504) | 0.250±0.001 (0.253) |
| diversity | 0.889±0.047 (0.829) | 0.535±0.094 (0.541) | 0.252±0.018 (0.250) |
| hybrid | 0.928±0.050 (0.858) | 0.514±0.144 (0.512) | 0.252±0.011 (0.252) |
| cost_uncertainty | 0.917±0.039 (0.840) | 0.490±0.110 (0.480) | 0.248±0.004 (0.251) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 12 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| uncertainty | +0.005 [-0.007, +0.018] p=0.43 (Holm 1.00) | -0.040 [-0.066, -0.013] p=0.01 (Holm 0.15) | +0.004 [-0.000, +0.008] p=0.13 (Holm 1.00) |
| diversity | -0.010 [-0.025, +0.008] p=0.19 (Holm 1.00) | -0.003 [-0.033, +0.030] p=0.77 (Holm 1.00) | +0.000 [-0.007, +0.008] p=1.00 (Holm 1.00) |
| hybrid | +0.020 [+0.006, +0.035] p=0.03 (Holm 0.27) | -0.032 [-0.060, -0.003] p=0.11 (Holm 0.95) | +0.003 [-0.001, +0.007] p=0.46 (Holm 1.00) |
| cost_uncertainty | +0.001 [-0.019, +0.024] p=1.00 (Holm 1.00) | -0.064 [-0.087, -0.044] p=0.00 (Holm 0.02) | +0.001 [-0.002, +0.005] p=0.74 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| random | 0.041±0.011 (0.059) | 0.317±0.107 (0.296) | 0.704±0.058 (0.702) |
| uncertainty | 0.035±0.014 (0.071) | 0.360±0.121 (0.366) | 0.728±0.053 (0.695) |
| diversity | 0.038±0.019 (0.066) | 0.320±0.098 (0.310) | 0.655±0.098 (0.671) |
| hybrid | 0.043±0.018 (0.062) | 0.347±0.146 (0.352) | 0.685±0.088 (0.693) |
| cost_uncertainty | 0.035±0.009 (0.067) | 0.385±0.107 (0.389) | 0.715±0.056 (0.714) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 12 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| uncertainty | +0.012 [+0.003, +0.022] p=0.04 (Holm 0.33) | +0.070 [+0.045, +0.094] p=0.00 (Holm 0.02) | -0.006 [-0.039, +0.022] p=1.00 (Holm 1.00) |
| diversity | +0.007 [-0.003, +0.019] p=0.56 (Holm 1.00) | +0.013 [-0.013, +0.037] p=0.49 (Holm 1.00) | -0.030 [-0.068, +0.002] p=0.23 (Holm 1.00) |
| hybrid | +0.003 [-0.007, +0.013] p=0.92 (Holm 1.00) | +0.056 [+0.025, +0.085] p=0.01 (Holm 0.10) | -0.009 [-0.047, +0.019] p=0.85 (Holm 1.00) |
| cost_uncertainty | +0.007 [-0.003, +0.017] p=0.43 (Holm 1.00) | +0.092 [+0.071, +0.117] p=0.00 (Holm 0.02) | +0.013 [-0.012, +0.036] p=0.19 (Holm 1.00) |
