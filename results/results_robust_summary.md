## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| random | 0.756±0.051 (0.696) | 0.535±0.068 (0.495) | 0.369±0.082 (0.350) |
| uncertainty | 0.779±0.067 (0.699) | 0.492±0.076 (0.448) | 0.387±0.069 (0.351) |
| diversity | 0.790±0.042 (0.721) | 0.516±0.067 (0.472) | 0.385±0.080 (0.371) |
| hybrid | 0.790±0.056 (0.712) | 0.495±0.070 (0.455) | 0.380±0.077 (0.337) |
| cost_uncertainty | 0.761±0.078 (0.694) | 0.476±0.057 (0.445) | 0.337±0.070 (0.319) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | scale_shift | source_shift |
|---|---|---|---|
| uncertainty | +0.003 (p=0.94) | -0.047 (p=0.00) | +0.001 (p=1.00) |
| diversity | +0.025 (p=0.02) | -0.023 (p=0.13) | +0.021 (p=0.19) |
| hybrid | +0.016 (p=0.19) | -0.040 (p=0.04) | -0.013 (p=0.77) |
| cost_uncertainty | -0.003 (p=0.92) | -0.050 (p=0.08) | -0.031 (p=0.05) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| random | 0.096±0.038 (0.144) | 0.308±0.072 (0.336) | 0.519±0.147 (0.523) |
| uncertainty | 0.113±0.058 (0.174) | 0.411±0.087 (0.431) | 0.500±0.094 (0.539) |
| diversity | 0.050±0.014 (0.095) | 0.324±0.078 (0.352) | 0.466±0.147 (0.474) |
| hybrid | 0.098±0.032 (0.150) | 0.392±0.063 (0.418) | 0.535±0.103 (0.576) |
| cost_uncertainty | 0.130±0.063 (0.173) | 0.426±0.051 (0.433) | 0.577±0.124 (0.585) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | scale_shift_ece | source_shift_ece |
|---|---|---|---|
| uncertainty | +0.031 (p=0.03) | +0.095 (p=0.00) | +0.016 (p=0.56) |
| diversity | -0.048 (p=0.00) | +0.016 (p=0.28) | -0.049 (p=0.11) |
| hybrid | +0.006 (p=0.70) | +0.082 (p=0.00) | +0.053 (p=0.11) |
| cost_uncertainty | +0.029 (p=0.19) | +0.097 (p=0.00) | +0.062 (p=0.05) |

## Mean top-label confidence (compare with accuracy: overconfidence under shift)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_conf | scale_shift_conf | source_shift_conf |
|---|---|---|---|
| random | 0.843±0.032 (0.832) | 0.840±0.038 (0.829) | 0.885±0.077 (0.871) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_conf | scale_shift_conf | source_shift_conf |
|---|---|---|---|