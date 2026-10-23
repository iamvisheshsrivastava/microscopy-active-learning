## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| random | 0.844±0.019 (0.775) | 0.557±0.049 (0.523) | 0.278±0.040 (0.281) |
| uncertainty | 0.860±0.029 (0.784) | 0.554±0.057 (0.534) | 0.264±0.026 (0.262) |
| diversity | 0.834±0.064 (0.757) | 0.529±0.061 (0.513) | 0.267±0.034 (0.272) |
| hybrid | 0.881±0.031 (0.790) | 0.549±0.044 (0.525) | 0.276±0.041 (0.267) |
| cost_uncertainty | 0.753±0.043 (0.716) | 0.525±0.059 (0.524) | 0.268±0.035 (0.273) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 12 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| uncertainty | +0.008 [-0.017, +0.029] p=0.43 (Holm 1.00) | +0.011 [-0.016, +0.037] p=0.49 (Holm 1.00) | -0.019 [-0.038, +0.000] p=0.07 (Holm 0.82) |
| diversity | -0.018 [-0.046, +0.011] p=0.28 (Holm 1.00) | -0.010 [-0.040, +0.021] p=0.56 (Holm 1.00) | -0.009 [-0.025, +0.006] p=0.28 (Holm 1.00) |
| hybrid | +0.015 [-0.004, +0.032] p=0.16 (Holm 1.00) | +0.002 [-0.018, +0.027] p=0.70 (Holm 1.00) | -0.014 [-0.028, +0.000] p=0.11 (Holm 1.00) |
| cost_uncertainty | -0.060 [-0.091, -0.032] p=0.00 (Holm 0.05) | +0.001 [-0.035, +0.035] p=0.70 (Holm 1.00) | -0.007 [-0.035, +0.019] p=0.77 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| random | 0.052±0.011 (0.083) | 0.305±0.046 (0.311) | 0.657±0.112 (0.646) |
| uncertainty | 0.064±0.023 (0.095) | 0.341±0.060 (0.325) | 0.686±0.072 (0.703) |
| diversity | 0.054±0.030 (0.079) | 0.309±0.066 (0.298) | 0.694±0.096 (0.652) |
| hybrid | 0.042±0.017 (0.083) | 0.338±0.042 (0.327) | 0.658±0.095 (0.679) |
| cost_uncertainty | 0.168±0.046 (0.149) | 0.385±0.062 (0.348) | 0.701±0.078 (0.677) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 12 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| uncertainty | +0.013 [-0.005, +0.036] p=0.43 (Holm 1.00) | +0.014 [-0.012, +0.045] p=0.92 (Holm 1.00) | +0.056 [-0.000, +0.112] p=0.11 (Holm 1.00) |
| diversity | -0.004 [-0.020, +0.013] p=0.77 (Holm 1.00) | -0.013 [-0.049, +0.021] p=0.56 (Holm 1.00) | +0.006 [-0.039, +0.050] p=0.85 (Holm 1.00) |
| hybrid | -0.000 [-0.016, +0.017] p=0.92 (Holm 1.00) | +0.017 [-0.010, +0.039] p=0.23 (Holm 1.00) | +0.033 [-0.004, +0.072] p=0.23 (Holm 1.00) |
| cost_uncertainty | +0.066 [+0.036, +0.099] p=0.00 (Holm 0.02) | +0.037 [+0.001, +0.075] p=0.05 (Holm 0.54) | +0.031 [-0.036, +0.101] p=0.43 (Holm 1.00) |
