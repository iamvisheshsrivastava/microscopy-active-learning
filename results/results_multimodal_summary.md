Mean±std over 5 seeds (each seed = mean of 5 random label draws). Retrieval chance = 1/300 = 0.003.

### 16 labels

| encoder | in_dist_acc | source_shift_acc | in_dist_r2 | source_shift_r2 | in_dist_cov90 | source_shift_cov90 |
|---|---|---|---|---|---|---|
| random_init | 0.677±0.048 | 0.276±0.006 | 0.526±0.086 | -0.157±0.107 | 0.846±0.048 | 0.911±0.030 |
| simclr_sem | 0.615±0.039 | 0.345±0.031 | 0.560±0.055 | -0.022±0.180 | 0.838±0.041 | 0.775±0.052 |
| clip_sem_ebsd | 0.687±0.019 | 0.313±0.032 | 0.660±0.035 | 0.029±0.122 | 0.838±0.026 | 0.773±0.025 |

### 48 labels

| encoder | in_dist_acc | source_shift_acc | in_dist_r2 | source_shift_r2 | in_dist_cov90 | source_shift_cov90 |
|---|---|---|---|---|---|---|
| random_init | 0.839±0.031 | 0.277±0.023 | 0.701±0.061 | -0.021±0.021 | 0.878±0.017 | 0.950±0.021 |
| simclr_sem | 0.716±0.023 | 0.368±0.057 | 0.640±0.046 | -0.128±0.196 | 0.866±0.021 | 0.716±0.028 |
| clip_sem_ebsd | 0.807±0.019 | 0.334±0.031 | 0.742±0.012 | -0.179±0.149 | 0.872±0.031 | 0.695±0.045 |

Cross-modal SEM->EBSD retrieval on 300 held-out pairs (chance: R@1 0.003, R@10 0.033, class-match 0.25):

| test set | R@1 | R@10 | top-1 class match |
|---|---|---|---|
| in_dist | 0.005 | 0.059 | 0.453 |
| source_shift | 0.004 | 0.045 | 0.292 |