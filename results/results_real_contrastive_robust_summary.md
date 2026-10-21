Encoder: contrastive (norm_input=True, strong_aug=True); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.528±0.068 (0.522) | 0.398±0.131 (0.360) | 0.180±0.087 (0.194) |
| uncertainty | 0.532±0.068 (0.506) | 0.411±0.100 (0.359) | 0.196±0.122 (0.240) |
| diversity | 0.549±0.070 (0.526) | 0.390±0.069 (0.351) | 0.189±0.091 (0.221) |
| hybrid | 0.551±0.070 (0.526) | 0.382±0.069 (0.321) | 0.178±0.089 (0.207) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.017 (p=0.43) | -0.001 (p=0.92) | +0.045 (p=0.11) |
| diversity | +0.004 (p=0.85) | -0.009 (p=0.92) | +0.027 (p=0.28) |
| hybrid | +0.004 (p=0.56) | -0.039 (p=0.28) | +0.012 (p=0.70) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.291±0.047 (0.285) | 0.211±0.061 (0.181) | 0.154±0.081 (0.177) |
| uncertainty | 0.283±0.059 (0.289) | 0.185±0.059 (0.185) | 0.157±0.080 (0.216) |
| diversity | 0.314±0.078 (0.278) | 0.155±0.029 (0.152) | 0.177±0.060 (0.210) |
| hybrid | 0.288±0.059 (0.275) | 0.155±0.034 (0.144) | 0.159±0.083 (0.176) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | +0.005 (p=0.70) | +0.004 (p=0.92) | +0.039 (p=0.16) |
| diversity | -0.006 (p=0.70) | -0.029 (p=0.06) | +0.033 (p=0.05) |
| hybrid | -0.009 (p=0.43) | -0.037 (p=0.01) | -0.000 (p=0.92) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.233±0.069 (0.266) | 0.353±0.108 (0.429) | 0.607±0.086 (0.616) |
| uncertainty | 0.263±0.065 (0.310) | 0.375±0.114 (0.453) | 0.623±0.118 (0.588) |
| diversity | 0.211±0.061 (0.244) | 0.319±0.091 (0.396) | 0.559±0.121 (0.551) |
| hybrid | 0.214±0.075 (0.271) | 0.386±0.084 (0.462) | 0.611±0.111 (0.603) |

ALC difference vs `random` (mean diff, Wilcoxon p; p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.044 (p=0.03) | +0.025 (p=0.56) | -0.028 (p=0.38) |
| diversity | -0.022 (p=0.23) | -0.032 (p=0.23) | -0.065 (p=0.13) |
| hybrid | +0.005 (p=0.85) | +0.034 (p=0.38) | -0.013 (p=0.77) |