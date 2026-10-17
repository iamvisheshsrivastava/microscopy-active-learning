import numpy as np
import pytest
import torch

from maldl.active.loop import run_loop
from maldl.active.strategies import STRATEGIES
from maldl.data.synthetic import NUM_CLASSES, make_dataset
from maldl.models.encoder import Encoder
from maldl.training.contrastive import embed, nt_xent, pretrain


def test_dataset_shapes_and_balance():
    x, y = make_dataset(40, seed=0, size=32)
    assert x.shape == (40, 1, 32, 32) and x.dtype == np.float32
    assert 0.0 <= x.min() and x.max() <= 1.0
    assert np.bincount(y, minlength=NUM_CLASSES).tolist() == [10] * NUM_CLASSES


def test_dataset_seed_determinism():
    a, ya = make_dataset(12, seed=3, size=32)
    b, yb = make_dataset(12, seed=3, size=32)
    c, _ = make_dataset(12, seed=4, size=32)
    assert np.array_equal(a, b) and np.array_equal(ya, yb)
    assert not np.array_equal(a, c)


def test_encoder_shape():
    z = Encoder(dim=128)(torch.zeros(5, 1, 64, 64))
    assert z.shape == (5, 128)


def test_nt_xent_prefers_matched_pairs():
    torch.manual_seed(0)
    z = torch.randn(16, 8)
    assert nt_xent(z, z + 0.01 * torch.randn_like(z)) < nt_xent(z, torch.randn(16, 8))


def _fake_state(n=60, d=8, seed=0):
    rng = np.random.default_rng(seed)
    y = np.arange(n) % NUM_CLASSES
    emb = rng.normal(size=(n, d)) + 3 * np.eye(NUM_CLASSES, d)[y]
    probs = rng.dirichlet(np.ones(NUM_CLASSES), size=n)
    return emb, probs, y


@pytest.mark.parametrize("name", list(STRATEGIES))
def test_strategy_unique_unlabeled(name):
    emb, probs, _ = _fake_state()
    labeled = np.arange(8)
    unlabeled = np.arange(8, 60)
    pick = STRATEGIES[name](emb, probs, labeled, unlabeled, 8, np.random.default_rng(0))
    assert len(pick) == 8 and len(set(pick.tolist())) == 8
    assert set(pick.tolist()) <= set(unlabeled.tolist())


@pytest.mark.parametrize("name", list(STRATEGIES))
def test_loop_never_relabels_and_is_deterministic(name):
    emb, _, y = _fake_state(80)
    ev = {"in_dist": (emb, y)}
    r1 = run_loop(emb, y, ev, name, init=8, batch=4, rounds=3, seed=1)
    r2 = run_loop(emb, y, ev, name, init=8, batch=4, rounds=3, seed=1)
    assert r1 == r2
    assert [r["n_labeled"] for r in r1] == [8, 12, 16, 20]  # loop raises on relabeling


def test_end_to_end_smoke():
    torch.manual_seed(0)
    x, y = make_dataset(64, seed=0, size=32)
    enc = Encoder()
    hist = pretrain(enc, x, epochs=2, batch=32, seed=0)
    assert len(hist) == 2 and all(np.isfinite(hist))
    emb = embed(enc, x)
    assert emb.shape == (64, 128)
    rows = run_loop(emb, y, {"in_dist": (emb, y)}, "hybrid", init=8, batch=4, rounds=2, seed=0)
    assert len(rows) == 3 and 0.0 <= rows[-1]["in_dist"] <= 1.0
