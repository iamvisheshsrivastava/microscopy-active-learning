"""SimCLR-style self-supervised training with multi-scale random-resized crops."""
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn


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


def gaussian_blur(v, sigma):
    r = max(1, int(3 * sigma))
    k = torch.exp(-0.5 * (torch.arange(-r, r + 1, dtype=v.dtype) / sigma) ** 2)
    k = k / k.sum()
    c = v.shape[0]
    v = F.pad(v[None], (r, r, r, r), mode="reflect")
    v = F.conv2d(v, k.view(1, 1, 1, -1).repeat(c, 1, 1, 1), groups=c)
    v = F.conv2d(v, k.view(1, 1, -1, 1).repeat(c, 1, 1, 1), groups=c)
    return v[0]


def intensity_jitter(v, rng, strong=False):
    """Contrast/brightness/noise (and blur if strong) on a (1,H,W) SEM view."""
    lo, hi, off, noise = (0.3, 1.7, 0.3, 0.15) if strong else (0.6, 1.4, 0.15, 0.08)
    if strong and rng.random() < 0.5:
        v = gaussian_blur(v, float(rng.uniform(0.5, 2.0)))
    v = (v - 0.5) * rng.uniform(lo, hi) + 0.5 + rng.uniform(-off, off)
    return v + torch.from_numpy(rng.normal(0, rng.uniform(0, noise), v.shape).astype(np.float32))


def augment(x, rng, out=64, strong=False):
    v = random_resized_crop(x, rng, out)
    if rng.random() < 0.5:
        v = v.flip(-1)
    if rng.random() < 0.5:
        v = v.flip(-2)
    v = v.rot90(int(rng.integers(0, 4)), (1, 2))
    return intensity_jitter(v, rng, strong)


def nt_xent(z1, z2, tau=0.2):
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    n = z1.shape[0]
    sim = z @ z.T / tau
    sim = sim.masked_fill(torch.eye(2 * n, dtype=torch.bool, device=z.device), -1e9)
    tgt = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)]).to(z.device)
    return F.cross_entropy(sim, tgt)


def pretrain(encoder, images, epochs=15, batch=64, lr=2e-3, seed=0, tau=0.2,
             strong=False, device="cpu"):
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
    encoder.to(device)
    head.to(device)
    opt = torch.optim.Adam(list(encoder.parameters()) + list(head.parameters()), lr=lr)
    hist = []
    encoder.train()
    for _ in range(epochs):
        perm = rng.permutation(len(x))
        tot, cnt = 0.0, 0
        for s in range(0, len(perm) - batch + 1, batch):
            idx = perm[s:s + batch]
            v1 = torch.stack([augment(x[i], rng, out, strong) for i in idx]).to(device)
            v2 = torch.stack([augment(x[i], rng, out, strong) for i in idx]).to(device)
            loss = nt_xent(head(encoder(v1)), head(encoder(v2)), tau)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += loss.item()
            cnt += 1
        hist.append(tot / max(cnt, 1))
    encoder.eval().cpu()
    return hist


@torch.no_grad()
def embed(encoder, images, batch=256):
    encoder.eval()
    x = torch.from_numpy(images)
    return torch.cat([encoder(x[i:i + batch]) for i in range(0, len(x), batch)]).numpy()
