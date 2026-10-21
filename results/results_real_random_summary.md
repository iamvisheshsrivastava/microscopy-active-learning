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

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.009 (p=0.49) | +0.014 (p=0.62) | -0.023 (p=0.91) |
| diversity | +0.015 (p=0.77) | -0.073 (p=0.00) | +0.005 (p=0.77) |
| hybrid | +0.019 (p=0.16) | -0.007 (p=0.85) | +0.029 (p=0.43) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.311±0.050 (0.284) | 0.228±0.111 (0.195) | 0.314±0.124 (0.294) |
| uncertainty | 0.303±0.077 (0.284) | 0.187±0.090 (0.175) | 0.293±0.178 (0.274) |
| diversity | 0.295±0.059 (0.284) | 0.212±0.114 (0.173) | 0.244±0.067 (0.283) |
| hybrid | 0.307±0.069 (0.282) | 0.185±0.091 (0.176) | 0.289±0.193 (0.330) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.000 (p=0.92) | -0.021 (p=0.13) | -0.020 (p=0.92) |
| diversity | -0.000 (p=1.00) | -0.023 (p=0.28) | -0.010 (p=1.00) |
| hybrid | -0.002 (p=0.62) | -0.019 (p=0.38) | +0.036 (p=0.28) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.156±0.060 (0.214) | 0.370±0.102 (0.464) | 0.388±0.144 (0.420) |
| uncertainty | 0.244±0.070 (0.285) | 0.449±0.117 (0.503) | 0.454±0.222 (0.487) |
| diversity | 0.156±0.061 (0.183) | 0.419±0.091 (0.482) | 0.392±0.117 (0.381) |
| hybrid | 0.174±0.056 (0.218) | 0.408±0.111 (0.479) | 0.411±0.176 (0.394) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.072 (p=0.00) | +0.039 (p=0.05) | +0.067 (p=0.11) |
| diversity | -0.031 (p=0.02) | +0.018 (p=0.19) | -0.040 (p=0.19) |
| hybrid | +0.005 (p=0.85) | +0.015 (p=0.56) | -0.026 (p=0.43) |