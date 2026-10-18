import torch.nn as nn


class Encoder(nn.Module):
    """Small CNN: 3 conv blocks, global average pool, linear to `dim`.

    norm_input: standardize every image (per-sample mean/std) before the first conv.
    This removes global contrast/brightness differences between instruments.
    """

    def __init__(self, dim=128, in_ch=1, norm_input=False):
        super().__init__()

        def block(i, o):
            return nn.Sequential(nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o),
                                 nn.ReLU(), nn.MaxPool2d(2))

        self.dim = dim
        self.norm_input = norm_input
        self.features = nn.Sequential(block(in_ch, 16), block(16, 32), block(32, 64))
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(64, dim)

    def forward(self, x):
        if self.norm_input:
            m = x.mean(dim=(1, 2, 3), keepdim=True)
            s = x.std(dim=(1, 2, 3), keepdim=True)
            x = (x - m) / (s + 1e-6)
        return self.fc(self.pool(self.features(x)).flatten(1))
