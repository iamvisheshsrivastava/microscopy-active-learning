"""Group-aware splits. Real micrographs from one sample/specimen must never be in both
train and test (near-duplicate fields of view inflate accuracy)."""
import numpy as np


def group_split(groups, test_frac=0.3, seed=0):
    """Split indices so that no group appears on both sides. Returns (train_idx, test_idx)."""
    groups = np.asarray(groups)
    uniq = np.unique(groups)
    if len(uniq) < 2:
        raise ValueError("need at least 2 groups to split")
    rng = np.random.default_rng(seed)
    rng.shuffle(uniq)
    n_test = min(len(uniq) - 1, max(1, round(test_frac * len(uniq))))
    test_groups = set(uniq[:n_test].tolist())
    is_test = np.array([g in test_groups for g in groups.tolist()])
    return np.flatnonzero(~is_test), np.flatnonzero(is_test)


def leave_one_group_out(groups):
    """Yield (train_idx, test_idx) with each group held out once (e.g. leave-one-instrument-out)."""
    groups = np.asarray(groups)
    for g in np.unique(groups):
        yield np.flatnonzero(groups != g), np.flatnonzero(groups == g)
