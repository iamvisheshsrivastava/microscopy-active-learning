Encoder: pretrained (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.722±0.068 (0.703) | 0.569±0.131 (0.511) | 0.666±0.178 (0.616) |
| uncertainty | 0.718±0.058 (0.707) | 0.575±0.073 (0.544) | 0.664±0.169 (0.611) |
| diversity | 0.732±0.061 (0.713) | 0.601±0.097 (0.559) | 0.664±0.179 (0.628) |
| hybrid | 0.736±0.064 (0.720) | 0.577±0.085 (0.554) | 0.644±0.174 (0.637) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | +0.004 [-0.013, +0.020] p=0.92 (Holm 1.00) | +0.034 [-0.007, +0.096] p=0.38 (Holm 1.00) | -0.005 [-0.033, +0.023] p=0.77 (Holm 1.00) |
| diversity | +0.010 [-0.010, +0.027] p=0.32 (Holm 1.00) | +0.048 [-0.002, +0.114] p=0.23 (Holm 1.00) | +0.012 [-0.025, +0.050] p=0.56 (Holm 1.00) |
| hybrid | +0.017 [-0.000, +0.035] p=0.13 (Holm 1.00) | +0.043 [-0.012, +0.113] p=0.43 (Holm 1.00) | +0.021 [-0.029, +0.074] p=0.56 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.395±0.053 (0.379) | 0.394±0.114 (0.288) | 0.549±0.273 (0.515) |
| uncertainty | 0.386±0.064 (0.395) | 0.333±0.079 (0.297) | 0.568±0.248 (0.528) |
| diversity | 0.412±0.097 (0.398) | 0.339±0.051 (0.292) | 0.562±0.266 (0.538) |
| hybrid | 0.437±0.083 (0.401) | 0.316±0.067 (0.297) | 0.555±0.257 (0.544) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | +0.016 [-0.009, +0.041] p=0.28 (Holm 1.00) | +0.009 [-0.038, +0.069] p=1.00 (Holm 1.00) | +0.012 [-0.017, +0.044] p=0.56 (Holm 1.00) |
| diversity | +0.020 [-0.003, +0.041] p=0.16 (Holm 1.00) | +0.004 [-0.039, +0.063] p=0.70 (Holm 1.00) | +0.023 [-0.010, +0.056] p=0.32 (Holm 1.00) |
| hybrid | +0.022 [+0.004, +0.039] p=0.06 (Holm 0.58) | +0.009 [-0.039, +0.072] p=1.00 (Holm 1.00) | +0.029 [-0.009, +0.069] p=0.32 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.172±0.057 (0.180) | 0.251±0.110 (0.288) | 0.218±0.109 (0.259) |
| uncertainty | 0.179±0.052 (0.176) | 0.268±0.066 (0.275) | 0.222±0.105 (0.256) |
| diversity | 0.158±0.039 (0.161) | 0.233±0.086 (0.255) | 0.217±0.106 (0.224) |
| hybrid | 0.163±0.050 (0.158) | 0.262±0.073 (0.267) | 0.223±0.113 (0.224) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | -0.004 [-0.012, +0.005] p=0.56 (Holm 1.00) | -0.013 [-0.063, +0.021] p=0.77 (Holm 1.00) | -0.003 [-0.026, +0.020] p=0.85 (Holm 1.00) |
| diversity | -0.019 [-0.032, -0.006] p=0.03 (Holm 0.22) | -0.033 [-0.092, +0.012] p=0.32 (Holm 1.00) | -0.035 [-0.066, -0.007] p=0.08 (Holm 0.59) |
| hybrid | -0.022 [-0.032, -0.010] p=0.01 (Holm 0.09) | -0.022 [-0.075, +0.019] p=0.92 (Holm 1.00) | -0.035 [-0.069, -0.003] p=0.13 (Holm 0.79) |
