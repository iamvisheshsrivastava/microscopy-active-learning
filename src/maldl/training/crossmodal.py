"""CLIP-style cross-modal contrastive training on registered SEM/EBSD pairs.

Both modalities share the same random-resized crop (they are spatially registered);
intensity jitter is applied to the SEM channel only. No flips/rotations, because
the EBSD channels encode orientation angles and would no longer match.
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .contrastive import intensity_jitter, random_resized_crop


def pair_augment(sem, ebsd, rng, out=64, strong=False):
    v = random_resized_crop(torch.cat([sem, ebsd]), rng, out)
    return intensity_jitter(v[:1], rng, strong), v[1:]


def clip_loss(za, zb, tau=0.2):
    za, zb = F.normalize(za, dim=1), F.normalize(zb, dim=1)
    logits = za @ zb.T / tau
    tgt = torch.arange(len(za), device=za.device)
    return 0.5 * (F.cross_entropy(logits, tgt) + F.cross_entropy(logits.T, tgt))


def pretrain_crossmodal(enc_sem, enc_ebsd, sem, ebsd, epochs=15, batch=64, lr=2e-3,
                        seed=0, tau=0.2, strong=False, device="cpu"):
    """Trains both encoders in place; returns loss history."""
    if epochs <= 0:
        enc_sem.eval(), enc_ebsd.eval()
        return []
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    xs, xe = torch.from_numpy(sem), torch.from_numpy(ebsd)
    out = xs.shape[-1]
    hs = nn.Sequential(nn.Linear(enc_sem.dim, 128), nn.ReLU(), nn.Linear(128, 64))
    he = nn.Sequential(nn.Linear(enc_ebsd.dim, 128), nn.ReLU(), nn.Linear(128, 64))
    mods = [enc_sem, enc_ebsd, hs, he]
    for m in mods:
        m.to(device).train()
    opt = torch.optim.Adam([p for m in mods for p in m.parameters()], lr=lr)
    hist = []
    for _ in range(epochs):
        perm = rng.permutation(len(xs))
        tot, cnt = 0.0, 0
        for s in range(0, len(perm) - batch + 1, batch):
            pairs = [pair_augment(xs[i], xe[i], rng, out, strong) for i in perm[s:s + batch]]
            a = torch.stack([p[0] for p in pairs]).to(device)
            b = torch.stack([p[1] for p in pairs]).to(device)
            loss = clip_loss(hs(enc_sem(a)), he(enc_ebsd(b)), tau)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += loss.item()
            cnt += 1
        hist.append(tot / max(cnt, 1))
    for m in mods:
        m.eval().cpu()
    enc_sem.proj, enc_ebsd.proj = hs, he  # aligned space lives after the heads
    return hist


@torch.no_grad()
def embed_projected(encoder, images, batch=256):
    """Embeddings in the aligned cross-modal space (encoder followed by its projection head)."""
    x = torch.from_numpy(images)
    return torch.cat([encoder.proj(encoder(x[i:i + batch]))
                      for i in range(0, len(x), batch)]).numpy()


def retrieval_class_match(emb_a, emb_b, y):
    """Fraction of rows whose top-1 retrieved item in the other modality has the same class."""
    a = emb_a / np.linalg.norm(emb_a, axis=1, keepdims=True)
    b = emb_b / np.linalg.norm(emb_b, axis=1, keepdims=True)
    return float((y[(a @ b.T).argmax(1)] == y).mean())


def retrieval_recall(emb_a, emb_b, k=1):
    """Fraction of rows whose paired item is within the top-k by cosine similarity (a -> b)."""
    a = emb_a / np.linalg.norm(emb_a, axis=1, keepdims=True)
    b = emb_b / np.linalg.norm(emb_b, axis=1, keepdims=True)
    sim = a @ b.T
    rank = (sim > np.diag(sim)[:, None]).sum(1)
    return float((rank < k).mean())
