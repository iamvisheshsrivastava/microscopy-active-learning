## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| random | 0.756±0.051 (0.696) | 0.535±0.068 (0.495) | 0.369±0.082 (0.350) |
| uncertainty | 0.779±0.067 (0.699) | 0.492±0.076 (0.448) | 0.387±0.069 (0.351) |
| diversity | 0.790±0.042 (0.721) | 0.516±0.067 (0.472) | 0.385±0.080 (0.371) |
| hybrid | 0.790±0.056 (0.712) | 0.495±0.070 (0.455) | 0.380±0.077 (0.337) |
| cost_uncertainty | 0.761±0.078 (0.694) | 0.476±0.057 (0.445) | 0.337±0.070 (0.319) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 12 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| uncertainty | +0.003 [-0.015, +0.022] p=0.94 (Holm 1.00) | -0.047 [-0.068, -0.027] p=0.00 (Holm 0.02) | +0.001 [-0.023, +0.026] p=1.00 (Holm 1.00) |
| diversity | +0.025 [+0.009, +0.039] p=0.02 (Holm 0.21) | -0.023 [-0.047, -0.004] p=0.13 (Holm 0.92) | +0.021 [-0.005, +0.046] p=0.19 (Holm 1.00) |
| hybrid | +0.016 [+0.001, +0.032] p=0.19 (Holm 1.00) | -0.040 [-0.068, -0.011] p=0.04 (Holm 0.37) | -0.013 [-0.047, +0.013] p=0.77 (Holm 1.00) |
| cost_uncertainty | -0.003 [-0.029, +0.022] p=0.92 (Holm 1.00) | -0.050 [-0.091, -0.011] p=0.08 (Holm 0.67) | -0.031 [-0.055, -0.006] p=0.05 (Holm 0.44) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| random | 0.096±0.038 (0.144) | 0.308±0.072 (0.336) | 0.519±0.147 (0.523) |
| uncertainty | 0.113±0.058 (0.174) | 0.411±0.087 (0.431) | 0.500±0.094 (0.539) |
| diversity | 0.050±0.014 (0.095) | 0.324±0.078 (0.352) | 0.466±0.147 (0.474) |
| hybrid | 0.098±0.032 (0.150) | 0.392±0.063 (0.418) | 0.535±0.103 (0.576) |
| cost_uncertainty | 0.130±0.063 (0.173) | 0.426±0.051 (0.433) | 0.577±0.124 (0.585) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 12 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| uncertainty | +0.031 [+0.010, +0.052] p=0.03 (Holm 0.22) | +0.095 [+0.067, +0.126] p=0.00 (Holm 0.02) | +0.016 [-0.032, +0.062] p=0.56 (Holm 1.00) |
| diversity | -0.048 [-0.068, -0.030] p=0.00 (Holm 0.04) | +0.016 [-0.011, +0.043] p=0.28 (Holm 0.83) | -0.049 [-0.100, +0.002] p=0.11 (Holm 0.63) |
| hybrid | +0.006 [-0.011, +0.025] p=0.70 (Holm 1.00) | +0.082 [+0.056, +0.107] p=0.00 (Holm 0.02) | +0.053 [+0.005, +0.116] p=0.11 (Holm 0.63) |
| cost_uncertainty | +0.029 [-0.002, +0.059] p=0.19 (Holm 0.77) | +0.097 [+0.057, +0.139] p=0.00 (Holm 0.04) | +0.062 [+0.012, +0.109] p=0.05 (Holm 0.34) |
