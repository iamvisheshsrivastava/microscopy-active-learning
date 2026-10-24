Encoder: random (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=128, mag_shift=107, detector_shift=34, pool=192
Majority-class accuracy (predict most frequent pool class): in_dist=0.348, mag_shift=0.170, detector_shift=0.300

## Accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.582±0.063 (0.536) | 0.371±0.111 (0.300) | 0.321±0.096 (0.293) |
| uncertainty | 0.585±0.066 (0.538) | 0.356±0.131 (0.305) | 0.274±0.118 (0.285) |
| diversity | 0.594±0.071 (0.545) | 0.331±0.063 (0.269) | 0.339±0.149 (0.319) |
| hybrid | 0.597±0.062 (0.543) | 0.386±0.114 (0.296) | 0.269±0.171 (0.286) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | +0.003 [-0.011, +0.016] p=0.62 (Holm 1.00) | +0.005 [-0.035, +0.039] p=0.77 (Holm 1.00) | -0.008 [-0.064, +0.046] p=0.77 (Holm 1.00) |
| diversity | +0.010 [-0.011, +0.027] p=0.32 (Holm 1.00) | -0.031 [-0.073, +0.013] p=0.28 (Holm 1.00) | +0.026 [-0.022, +0.078] p=0.62 (Holm 1.00) |
| hybrid | +0.007 [-0.012, +0.024] p=0.49 (Holm 1.00) | -0.004 [-0.042, +0.036] p=0.77 (Holm 1.00) | -0.007 [-0.068, +0.054] p=0.92 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.306±0.049 (0.290) | 0.261±0.082 (0.214) | 0.309±0.168 (0.277) |
| uncertainty | 0.313±0.052 (0.294) | 0.192±0.081 (0.192) | 0.277±0.163 (0.279) |
| diversity | 0.316±0.052 (0.307) | 0.213±0.074 (0.195) | 0.344±0.183 (0.323) |
| hybrid | 0.320±0.059 (0.299) | 0.230±0.099 (0.208) | 0.282±0.209 (0.299) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | +0.004 [-0.009, +0.016] p=0.77 (Holm 1.00) | -0.022 [-0.044, -0.000] p=0.11 (Holm 0.74) | +0.002 [-0.059, +0.055] p=0.92 (Holm 1.00) |
| diversity | +0.017 [+0.002, +0.034] p=0.05 (Holm 0.44) | -0.019 [-0.044, +0.005] p=0.19 (Holm 1.00) | +0.046 [+0.005, +0.090] p=0.08 (Holm 0.67) |
| hybrid | +0.008 [-0.010, +0.028] p=0.32 (Holm 1.00) | -0.006 [-0.044, +0.034] p=0.85 (Holm 1.00) | +0.022 [-0.037, +0.081] p=0.77 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 10 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.142±0.064 (0.200) | 0.383±0.087 (0.469) | 0.404±0.140 (0.465) |
| uncertainty | 0.191±0.079 (0.251) | 0.466±0.136 (0.514) | 0.472±0.129 (0.527) |
| diversity | 0.128±0.040 (0.167) | 0.346±0.095 (0.430) | 0.396±0.139 (0.406) |
| hybrid | 0.149±0.060 (0.217) | 0.411±0.100 (0.488) | 0.497±0.159 (0.501) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.002 with 10 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.051 [+0.034, +0.069] p=0.00 (Holm 0.02) | +0.045 [+0.012, +0.080] p=0.08 (Holm 0.42) | +0.062 [+0.022, +0.113] p=0.02 (Holm 0.14) |
| diversity | -0.034 [-0.055, -0.013] p=0.02 (Holm 0.14) | -0.038 [-0.084, -0.000] p=0.16 (Holm 0.52) | -0.059 [-0.089, -0.034] p=0.00 (Holm 0.03) |
| hybrid | +0.016 [-0.005, +0.037] p=0.28 (Holm 0.52) | +0.019 [-0.021, +0.054] p=0.23 (Holm 0.52) | +0.036 [+0.000, +0.069] p=0.13 (Holm 0.52) |
