"""Frozen pretrained vision backbone (e.g. DINOv2) as an embedding function.

Weights are downloaded at run time from the Hugging Face hub (never in tests/CI).
Grayscale micrographs are replicated to 3 channels, resized and ImageNet-normalised.
Embedding = concat(CLS token, mean patch token).
"""
import numpy as np
import torch
import torch.nn.functional as F

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def preprocess_for_backbone(images, size=224):
    """(N,1,H,W) float in [0,1] -> (N,3,size,size) ImageNet-normalised tensor."""
    x = torch.as_tensor(np.asarray(images), dtype=torch.float32)
    if x.shape[1] == 1:
        x = x.repeat(1, 3, 1, 1)
    if x.shape[-1] != size or x.shape[-2] != size:
        x = F.interpolate(x, size=(size, size), mode="bilinear", align_corners=False)
    mean = torch.tensor(IMAGENET_MEAN).view(1, 3, 1, 1)
    std = torch.tensor(IMAGENET_STD).view(1, 3, 1, 1)
    return (x - mean) / std


class PretrainedBackbone:
    def __init__(self, name="facebook/dinov2-small", device="cpu", size=224):
        from transformers import AutoModel  # imported lazily: optional dependency
        self.model = AutoModel.from_pretrained(name).eval().to(device)
        self.device, self.size, self.name = device, size, name

    @torch.no_grad()
    def __call__(self, images, batch=64):
        out = []
        for i in range(0, len(images), batch):
            x = preprocess_for_backbone(images[i:i + batch], self.size).to(self.device)
            h = self.model(pixel_values=x).last_hidden_state
            out.append(torch.cat([h[:, 0], h[:, 1:].mean(1)], dim=1).float().cpu())
        return torch.cat(out).numpy()
