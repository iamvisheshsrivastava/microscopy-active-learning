import csv

import numpy as np
import pytest
import torch
from PIL import Image

from maldl.active.loop import run_loop, run_regression_loop
from maldl.active.strategies import STRATEGIES
from maldl.data.folder import load_table
from maldl.data.splits import group_split, leave_one_group_out
from maldl.data.synthetic import NUM_CLASSES, make_dataset, make_paired_dataset
from maldl.eval.calibration import ece, interval_coverage
from maldl.eval.stats import markdown_summary, paired_test
from maldl.models.encoder import Encoder
from maldl.models.surrogate import GPSurrogate
from maldl.training.contrastive import embed, nt_xent, pretrain
from maldl.training.crossmodal import (clip_loss, embed_projected, pretrain_crossmodal,
                                           retrieval_class_match, retrieval_recall)


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


def test_paired_dataset_and_property():
    sem, ebsd, y, info = make_paired_dataset(40, seed=0, size=32)
    assert sem.shape == (40, 1, 32, 32) and ebsd.shape == (40, 2, 32, 32)
    assert len(info["property"]) == len(info["cost"]) == 40
    assert info["cost"].min() >= 1.0
    # finer grains (class 0) are harder than coarse (class 1) on average (Hall-Petch)
    assert info["property"][y == 0].mean() > info["property"][y == 1].mean()
    # property is magnification-independent in expectation (physical grain size)
    _, _, i1 = make_dataset(200, 1, size=32, scale=1.0, return_info=True)
    _, _, i2 = make_dataset(200, 1, size=32, scale=1.5, return_info=True)
    assert abs(i1["property"].mean() - i2["property"].mean()) < 40


@pytest.mark.parametrize("norm", [False, True])
def test_encoder_shape(norm):
    z = Encoder(dim=128, norm_input=norm)(torch.rand(5, 1, 64, 64))
    assert z.shape == (5, 128) and torch.isfinite(z).all()


def test_norm_input_removes_global_contrast():
    enc = Encoder(norm_input=True).eval()
    x = torch.rand(3, 1, 32, 32)
    assert torch.allclose(enc(x), enc(0.5 * x + 0.2), atol=1e-4)


def test_nt_xent_prefers_matched_pairs():
    torch.manual_seed(0)
    z = torch.randn(16, 8)
    assert nt_xent(z, z + 0.01 * torch.randn_like(z)) < nt_xent(z, torch.randn(16, 8))
    assert clip_loss(z, z + 0.01 * torch.randn_like(z)) < clip_loss(z, torch.randn(16, 8))


def _fake_state(n=60, d=8, seed=0):
    rng = np.random.default_rng(seed)
    y = np.arange(n) % NUM_CLASSES
    emb = rng.normal(size=(n, d)) + 3 * np.eye(NUM_CLASSES, d)[y]
    unc = rng.random(n)
    return emb, unc, y


@pytest.mark.parametrize("name", list(STRATEGIES))
def test_strategy_unique_unlabeled(name):
    emb, unc, _ = _fake_state()
    labeled, unlabeled = np.arange(8), np.arange(8, 60)
    cost = 1 + np.random.default_rng(1).random(60)
    pick = STRATEGIES[name](emb, unc, labeled, unlabeled, 8, np.random.default_rng(0), cost=cost)
    assert len(pick) == 8 and len(set(pick.tolist())) == 8
    assert set(pick.tolist()) <= set(unlabeled.tolist())


def test_cost_uncertainty_prefers_cheap_when_uncertainty_equal():
    emb, _, _ = _fake_state()
    unc, cost = np.ones(60), np.arange(1, 61, dtype=float)
    pick = STRATEGIES["cost_uncertainty"](emb, unc, np.arange(8), np.arange(8, 60), 4,
                                          np.random.default_rng(0), cost=cost)
    assert sorted(pick.tolist()) == [8, 9, 10, 11]


@pytest.mark.parametrize("name", list(STRATEGIES))
def test_loop_never_relabels_and_is_deterministic(name):
    emb, _, y = _fake_state(80)
    ev = {"in_dist": (emb, y, y.astype(float))}
    r1 = run_loop(emb, y, ev, name, init=8, batch=4, rounds=3, seed=1)
    r2 = run_loop(emb, y, ev, name, init=8, batch=4, rounds=3, seed=1)
    assert r1 == r2
    assert [r["n_labeled"] for r in r1] == [8, 12, 16, 20]  # loop raises on relabeling
    assert all(0 <= r["in_dist_ece"] <= 1 for r in r1)


def test_regression_loop_and_gp_uncertainty():
    rng = np.random.default_rng(0)
    emb = rng.normal(size=(120, 10))
    prop = emb[:, 0] * 3 + rng.normal(0, 0.1, 120)
    ev = {"in_dist": (emb, None, prop)}
    rows = run_regression_loop(emb, prop, ev, "uncertainty", init=8, batch=6, rounds=3, seed=0)
    assert [r["n_labeled"] for r in rows] == [8, 14, 20, 26]
    assert rows[-1]["in_dist_r2"] > 0.5
    gp = GPSurrogate(emb).fit(emb[:20], prop[:20])
    _, std = gp.predict(emb)
    assert (std > 0).all()


def test_calibration_metrics():
    p = np.eye(4)[np.arange(40) % 4] * 0.98 + 0.005
    assert ece(p, np.arange(40) % 4) < 0.03       # confident and right
    assert ece(p, (np.arange(40) + 1) % 4) > 0.9  # confident and wrong
    y = np.zeros(1000)
    m = np.random.default_rng(0).normal(size=1000)
    assert abs(interval_coverage(y, m, np.ones(1000)) - 0.90) < 0.04


def test_group_splits_never_leak():
    groups = np.repeat(np.arange(10), 5)
    tr, te = group_split(groups, 0.3, seed=0)
    assert not set(groups[tr]) & set(groups[te]) and len(tr) + len(te) == 50
    for tr, te in leave_one_group_out(groups):
        assert not set(groups[tr]) & set(groups[te])


def test_load_table(tmp_path):
    rows = []
    for i in range(4):
        Image.fromarray((np.random.default_rng(i).random((20, 20)) * 255).astype(np.uint8)
                        ).save(tmp_path / f"{i}.png")
        rows.append({"path": f"{i}.png", "label": "a" if i < 2 else "b",
                     "group": f"s{i // 2}"})
    with open(tmp_path / "meta.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "label", "group"])
        w.writeheader()
        w.writerows(rows)
    x, y, classes, meta = load_table(tmp_path / "meta.csv", tmp_path, size=16)
    assert x.shape == (4, 1, 16, 16) and classes == ["a", "b"] and meta["group"][0] == "s0"


def test_stats_summary():
    rows = [{"strategy": s, "seed": sd, "round": r, "m": 0.5 + 0.1 * r + (0.05 if s == "b" else 0)
             + 0.01 * sd} for s in "ab" for sd in range(6) for r in range(3)]
    d, p = paired_test(np.arange(6) + 1.0, np.arange(6) * 1.0)
    assert d == 1.0 and p < 0.05
    md = markdown_summary(rows, ["a", "b"], ["m"], baseline="a")
    assert "+0.050" in md


def test_end_to_end_smoke():
    torch.manual_seed(0)
    sem, ebsd, y, info = make_paired_dataset(64, seed=0, size=32)
    enc = Encoder(norm_input=True)
    hist = pretrain(enc, sem, epochs=2, batch=32, seed=0, strong=True)
    assert len(hist) == 2 and all(np.isfinite(hist))
    emb = embed(enc, sem)
    assert emb.shape == (64, 128)
    ev = {"in_dist": (emb, y, info["property"])}
    rows = run_loop(emb, y, ev, "hybrid", init=8, batch=4, rounds=2, seed=0, costs=info["cost"])
    assert len(rows) == 3 and rows[-1]["cum_cost"] > rows[0]["cum_cost"]
    es, ee = Encoder(norm_input=True), Encoder(in_ch=2)
    h = pretrain_crossmodal(es, ee, sem, ebsd, epochs=2, batch=32, seed=0)
    assert len(h) == 2 and all(np.isfinite(h))
    r1 = retrieval_recall(embed_projected(es, sem), embed_projected(ee, ebsd))
    assert 0.0 <= r1 <= 1.0


def test_crossmodal_learns_alignment():
    """After a short training run, held-out SEM->EBSD retrieval must beat chance."""
    torch.manual_seed(0)
    sem, ebsd, _, _ = make_paired_dataset(192, seed=1, size=32)
    es, ee = Encoder(norm_input=True), Encoder(in_ch=2)
    pretrain_crossmodal(es, ee, sem, ebsd, epochs=10, batch=32, seed=0)
    ts, te, ty, _ = make_paired_dataset(100, seed=2, size=32)
    m = retrieval_class_match(embed_projected(es, ts), embed_projected(ee, te), ty)
    assert m > 0.4  # chance is 0.25
