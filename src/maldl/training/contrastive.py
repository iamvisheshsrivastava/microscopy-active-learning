"""SimCLR-style self-supervised training with multi-scale random-resized crops."""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def random_resized_crop(x, rng, out=64, scale=(0.15, 1.0)):
    """x: (C,H,W) tensor. Crop area fraction ~ U(scale), resize back to `out`."""
    _, h, w = x.shape
    frac = rng.uniform(*scale)
    ratio = np.exp(rng.uniform(np.log(3 / 4), np.log(4 / 3)))
    ch = int(min(h, max(8, round(np.sqrt(frac * h * w / ratio)))))
    cw = int(min(w, max(8, round(np.sqrt(frac * h * w * ratio)))))
    i = int(rng.integers(0, h - ch + 1))
    j = int(rng.integers(0, w - cw + 1))
    c = x[:, i:i + ch, j:j + cw][None]
    return F.interpolate(c, size=(out, out), mode="bilinear", align_corners=False)[0]


def augment(x, rng, out=64):
    v = random_resized_crop(x, rng, out)
    if rng.random() < 0.5:
        v = v.flip(-1)
    if rng.random() < 0.5:
        v = v.flip(-2)
    v = v.rot90(int(rng.integers(0, 4)), (1, 2))
    v = (v - 0.5) * rng.uniform(0.6, 1.4) + 0.5 + rng.uniform(-0.15, 0.15)
    v = v + torch.from_numpy(rng.normal(0, rng.uniform(0, 0.08), v.shape).astype(np.float32))
    return v


def nt_xent(z1, z2, tau=0.2):
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    n = z1.shape[0]
    sim = z @ z.T / tau
    sim = sim.masked_fill(torch.eye(2 * n, dtype=torch.bool), -1e9)
    tgt = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return F.cross_entropy(sim, tgt)


def pretrain(encoder, images, epochs=15, batch=64, lr=2e-3, seed=0, tau=0.2):
    """images: (N,C,H,W) numpy. Trains encoder in place; returns loss history."""
    if epochs <= 0:
        encoder.eval()
        return []
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    x = torch.from_numpy(images)
    out = x.shape[-1]
    # projection head is used only for the loss and discarded afterwards
    head = nn.Sequential(nn.Linear(encoder.dim, 128), nn.ReLU(), nn.Linear(128, 64))
    opt = torch.optim.Adam(list(encoder.parameters()) + list(head.parameters()), lr=lr)
    hist = []
    encoder.train()
    for _ in range(epochs):
        perm = rng.permutation(len(x))
        tot, cnt = 0.0, 0
        for s in range(0, len(perm) - batch + 1, batch):
            idx = perm[s:s + batch]
            v1 = torch.stack([augment(x[i], rng, out) for i in idx])
            v2 = torch.stack([augment(x[i], rng, out) for i in idx])
            loss = nt_xent(head(encoder(v1)), head(encoder(v2)), tau)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += loss.item()
            cnt += 1
        hist.append(tot / max(cnt, 1))
    encoder.eval()
    return hist


@torch.no_grad()
def embed(encoder, images, batch=256):
    encoder.eval()
    x = torch.from_numpy(images)
    return torch.cat([encoder(x[i:i + batch]) for i in range(0, len(x), batch)]).numpy()
