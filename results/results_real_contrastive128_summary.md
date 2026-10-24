Encoder: contrastive (norm_input=False, strong_aug=False); 7 classes; mean sizes: in_dist=126, mag_shift=101, detector_shift=32, pool=194
Majority-class accuracy (predict most frequent pool class): in_dist=0.310, mag_shift=0.341, detector_shift=0.230

## Accuracy

Final round, mean±std over 5 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| random | 0.590±0.078 (0.547) | 0.449±0.056 (0.367) | 0.352±0.186 (0.318) |
| uncertainty | 0.557±0.071 (0.515) | 0.319±0.134 (0.271) | 0.267±0.115 (0.282) |
| diversity | 0.604±0.056 (0.576) | 0.373±0.043 (0.282) | 0.229±0.069 (0.306) |
| hybrid | 0.585±0.066 (0.551) | 0.386±0.135 (0.315) | 0.354±0.166 (0.306) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.062 with 5 seeds).

| strategy | in_dist | mag_shift | detector_shift |
|---|---|---|---|
| uncertainty | -0.032 [-0.085, +0.022] p=0.44 (Holm 1.00) | -0.096 [-0.191, -0.001] p=0.31 (Holm 1.00) | -0.035 [-0.093, +0.025] p=0.31 (Holm 1.00) |
| diversity | +0.029 [-0.006, +0.057] p=0.19 (Holm 1.00) | -0.085 [-0.135, -0.038] p=0.06 (Holm 0.56) | -0.012 [-0.111, +0.081] p=1.00 (Holm 1.00) |
| hybrid | +0.004 [-0.055, +0.050] p=1.00 (Holm 1.00) | -0.052 [-0.154, +0.049] p=0.44 (Holm 1.00) | -0.012 [-0.067, +0.048] p=0.44 (Holm 1.00) |

## Balanced accuracy

Final round, mean±std over 5 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| random | 0.320±0.064 (0.322) | 0.252±0.082 (0.253) | 0.325±0.216 (0.282) |
| uncertainty | 0.321±0.087 (0.294) | 0.182±0.061 (0.188) | 0.214±0.109 (0.256) |
| diversity | 0.308±0.076 (0.292) | 0.218±0.088 (0.198) | 0.199±0.088 (0.265) |
| hybrid | 0.296±0.059 (0.289) | 0.198±0.057 (0.209) | 0.337±0.219 (0.282) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.062 with 5 seeds).

| strategy | in_dist_bacc | mag_shift_bacc | detector_shift_bacc |
|---|---|---|---|
| uncertainty | -0.028 [-0.058, -0.001] p=0.19 (Holm 1.00) | -0.064 [-0.100, -0.029] p=0.06 (Holm 0.56) | -0.026 [-0.070, +0.018] p=0.62 (Holm 1.00) |
| diversity | -0.030 [-0.072, +0.007] p=0.62 (Holm 1.00) | -0.054 [-0.086, -0.023] p=0.06 (Holm 0.56) | -0.017 [-0.116, +0.084] p=0.81 (Holm 1.00) |
| hybrid | -0.034 [-0.068, -0.004] p=0.19 (Holm 1.00) | -0.043 [-0.078, -0.014] p=0.06 (Holm 0.56) | -0.000 [-0.050, +0.049] p=1.00 (Holm 1.00) |

## Expected calibration error (lower is better)

Final round, mean±std over 5 seeds; ALC (mean over rounds) in parentheses.

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| random | 0.164±0.074 (0.249) | 0.295±0.074 (0.423) | 0.391±0.142 (0.433) |
| uncertainty | 0.251±0.058 (0.308) | 0.452±0.145 (0.555) | 0.488±0.065 (0.528) |
| diversity | 0.155±0.061 (0.205) | 0.316±0.071 (0.447) | 0.393±0.088 (0.425) |
| hybrid | 0.214±0.076 (0.261) | 0.367±0.126 (0.482) | 0.451±0.112 (0.488) |

ALC difference vs `random`: mean diff [95% bootstrap CI over seeds], Wilcoxon p, Holm-adjusted p over all 9 cells of this table (p cannot go below ~0.062 with 5 seeds).

| strategy | in_dist_ece | mag_shift_ece | detector_shift_ece |
|---|---|---|---|
| uncertainty | +0.059 [+0.014, +0.109] p=0.12 (Holm 1.00) | +0.133 [+0.029, +0.230] p=0.31 (Holm 1.00) | +0.095 [+0.023, +0.181] p=0.12 (Holm 1.00) |
| diversity | -0.045 [-0.073, -0.016] p=0.12 (Holm 1.00) | +0.025 [-0.022, +0.085] p=0.81 (Holm 1.00) | -0.008 [-0.075, +0.065] p=1.00 (Holm 1.00) |
| hybrid | +0.011 [-0.033, +0.062] p=0.81 (Holm 1.00) | +0.060 [-0.034, +0.157] p=0.44 (Holm 1.00) | +0.055 [+0.001, +0.109] p=0.31 (Holm 1.00) |
