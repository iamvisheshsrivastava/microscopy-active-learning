Encoder: random (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.563±0.072 (0.514) | 0.354±0.084 (0.284) | 0.401±0.164 (0.368) |
| uncertainty | 0.555±0.055 (0.505) | 0.352±0.093 (0.298) | 0.383±0.180 (0.345) |
| diversity | 0.558±0.059 (0.529) | 0.257±0.086 (0.211) | 0.321±0.121 (0.373) |
| hybrid | 0.571±0.048 (0.533) | 0.331±0.078 (0.277) | 0.358±0.205 (0.397) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.009 [-0.031, +0.014] p=0.49 (Holm 1.00) | +0.014 [-0.020, +0.054] p=0.62 (Holm 1.00) | -0.023 [-0.102, +0.029] p=0.91 (Holm 1.00) |
| diversity | +0.015 [-0.011, +0.043] p=0.77 (Holm 1.00) | -0.073 [-0.113, -0.038] p=0.00 (Holm 0.04) | +0.005 [-0.064, +0.071] p=0.77 (Holm 1.00) |
| hybrid | +0.019 [-0.002, +0.038] p=0.16 (Holm 1.00) | -0.007 [-0.035, +0.023] p=0.85 (Holm 1.00) | +0.029 [-0.025, +0.082] p=0.43 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.311±0.050 (0.284) | 0.228±0.111 (0.195) | 0.314±0.124 (0.294) |
| uncertainty | 0.303±0.077 (0.284) | 0.187±0.090 (0.175) | 0.293±0.178 (0.274) |
| diversity | 0.295±0.059 (0.284) | 0.212±0.114 (0.173) | 0.244±0.067 (0.283) |
| hybrid | 0.307±0.069 (0.282) | 0.185±0.091 (0.176) | 0.289±0.193 (0.330) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.000 [-0.023, +0.020] p=0.92 (Holm 1.00) | -0.021 [-0.044, +0.001] p=0.13 (Holm 1.00) | -0.020 [-0.081, +0.021] p=0.92 (Holm 1.00) |
| diversity | -0.000 [-0.015, +0.014] p=1.00 (Holm 1.00) | -0.023 [-0.053, +0.005] p=0.28 (Holm 1.00) | -0.010 [-0.071, +0.042] p=1.00 (Holm 1.00) |
| hybrid | -0.002 [-0.017, +0.011] p=0.62 (Holm 1.00) | -0.019 [-0.050, +0.012] p=0.38 (Holm 1.00) | +0.036 [-0.006, +0.084] p=0.28 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.156±0.060 (0.214) | 0.370±0.102 (0.464) | 0.388±0.144 (0.420) |
| uncertainty | 0.244±0.070 (0.285) | 0.449±0.117 (0.503) | 0.454±0.222 (0.487) |
| diversity | 0.156±0.061 (0.183) | 0.419±0.091 (0.482) | 0.392±0.117 (0.381) |
| hybrid | 0.174±0.056 (0.218) | 0.408±0.111 (0.479) | 0.411±0.176 (0.394) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.072 [+0.048, +0.098] p=0.00 (Holm 0.02) | +0.039 [+0.008, +0.065] p=0.05 (Holm 0.34) | +0.067 [-0.010, +0.182] p=0.11 (Holm 0.63) |
| diversity | -0.031 [-0.048, -0.013] p=0.02 (Holm 0.16) | +0.018 [-0.007, +0.044] p=0.19 (Holm 0.97) | -0.040 [-0.078, -0.002] p=0.19 (Holm 0.97) |
| hybrid | +0.005 [-0.023, +0.034] p=0.85 (Holm 1.00) | +0.015 [-0.013, +0.046] p=0.56 (Holm 1.00) | -0.026 [-0.084, +0.029] p=0.43 (Holm 1.00) |
