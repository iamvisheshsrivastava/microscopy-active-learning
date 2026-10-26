"""Build evaluation sets under scale shift and source (instrument) shift."""
from ..data.synthetic import SOURCE_A, SOURCE_B, make_dataset
from ..training.contrastive import embed


def build_eval_sets(encoder, seed, n=300, size=64, shift_scale=1.5):
    """Test sets use seeds disjoint from train.
    Returns {name: (emb, y_class, y_property)}."""
    specs = {
        "in_dist": {"scale": 1.0, "source": SOURCE_A},
        "scale_shift": {"scale": shift_scale, "source": SOURCE_A},
        "source_shift": {"scale": 1.0, "source": SOURCE_B},
    }
    out = {}
    for i, (name, kw) in enumerate(specs.items()):
        x, y, info = make_dataset(n, seed=10_000 + seed * 10 + i, size=size,
                                  return_info=True, **kw)
        out[name] = (embed(encoder, x), y, info["property"])
    return out
