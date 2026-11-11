import numpy as np
import pytest

from maldl.active.loop import run_loop
from maldl.active.strategies import (UNCERTAINTY_MEASURES, entropy,
                                     least_confidence, margin)

ONE_HOT = np.array([[1.0, 0.0, 0.0, 0.0]])
UNIFORM = np.array([[0.25, 0.25, 0.25, 0.25]])
MIXED = np.array([[0.5, 0.3, 0.2, 0.0]])


@pytest.mark.parametrize("measure", [entropy, least_confidence, margin])
def test_one_hot_is_least_uncertain_uniform_is_most(measure):
    assert measure(ONE_HOT)[0] == pytest.approx(0.0, abs=1e-9)
    assert measure(UNIFORM)[0] > measure(MIXED)[0] > measure(ONE_HOT)[0]


def test_measure_values():
    assert entropy(UNIFORM)[0] == pytest.approx(np.log(4))
    assert least_confidence(UNIFORM)[0] == pytest.approx(0.75)
    assert least_confidence(MIXED)[0] == pytest.approx(0.5)
    assert margin(UNIFORM)[0] == pytest.approx(1.0)
    assert margin(MIXED)[0] == pytest.approx(1.0 - (0.5 - 0.3))


def test_measures_return_one_score_per_row():
    probs = np.vstack([ONE_HOT, UNIFORM, MIXED])
    for measure in UNCERTAINTY_MEASURES.values():
        out = measure(probs)
        assert out.shape == (3,)


def _fake_pool(n=80, d=10, seed=0):
    rng = np.random.default_rng(seed)
    emb = rng.normal(size=(n, d))
    y = rng.integers(0, 4, n)
    ev = {"in_dist": (emb, y, y.astype(float))}
    return emb, y, ev


@pytest.mark.parametrize("name", list(UNCERTAINTY_MEASURES))
def test_run_loop_accepts_each_uncertainty_measure(name):
    emb, y, ev = _fake_pool()
    rows = run_loop(emb, y, ev, "uncertainty", init=8, batch=4, rounds=3,
                    seed=1, uncertainty=name)
    assert [r["n_labeled"] for r in rows] == [8, 12, 16, 20]


def test_run_loop_default_matches_explicit_entropy():
    emb, y, ev = _fake_pool()
    r_default = run_loop(emb, y, ev, "uncertainty", init=8, batch=4, rounds=3, seed=1)
    r_entropy = run_loop(emb, y, ev, "uncertainty", init=8, batch=4, rounds=3,
                         seed=1, uncertainty="entropy")
    assert r_default == r_entropy


def test_run_loop_invalid_uncertainty_raises():
    emb, y, ev = _fake_pool()
    with pytest.raises(ValueError, match="unknown uncertainty measure"):
        run_loop(emb, y, ev, "uncertainty", uncertainty="bogus")
