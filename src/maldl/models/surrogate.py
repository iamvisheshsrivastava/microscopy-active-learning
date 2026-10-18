"""Gaussian-process surrogate: embedding -> scalar property, with predictive uncertainty."""
import warnings

import numpy as np
from sklearn.decomposition import PCA
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.preprocessing import StandardScaler


class GPSurrogate:
    """The scaler/PCA are fit on the (label-free) pool embeddings, then reused for any split."""

    def __init__(self, pool_emb, n_components=16):
        self.sc = StandardScaler().fit(pool_emb)
        self.nc = min(n_components, pool_emb.shape[1])
        self.pca = PCA(self.nc, random_state=0).fit(self.sc.transform(pool_emb))
        self.scale = float(self.pca.transform(self.sc.transform(pool_emb)).std())
        self.gp = None

    def _t(self, emb):
        return self.pca.transform(self.sc.transform(emb)) / self.scale

    def fit(self, emb, y):
        k = ConstantKernel(1.0) * RBF(length_scale=np.sqrt(self.nc)) + WhiteKernel(0.1)
        self.gp = GaussianProcessRegressor(k, normalize_y=True, random_state=0)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.gp.fit(self._t(emb), y)
        return self

    def predict(self, emb):
        mean, std = self.gp.predict(self._t(emb), return_std=True)
        return mean, std
