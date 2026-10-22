"""Synthetic prototype: Gaussian density on a fixed covariance support.

No data loading or fitting is provided. Numerical cutoffs belong to the caller's
units-aware contract; prototype defaults are frozen for dimensionless controls.
"""
from dataclasses import dataclass
import math
import numpy as np


@dataclass
class SupportGaussian:
    positive_vectors: np.ndarray
    positive_eigenvalues: np.ndarray
    null_vectors: np.ndarray
    threshold: float
    support_tolerance: float

    @classmethod
    def from_covariance(cls, covariance, relative_cutoff=1e-12,
                        absolute_cutoff=0.0, support_tolerance=1e-10):
        c = np.asarray(covariance, dtype=float)
        if c.ndim != 2 or c.shape[0] != c.shape[1] or not np.isfinite(c).all():
            raise ValueError('Covariance must be a finite square matrix')
        def tolerance(value, name):
            raw = np.asarray(value, dtype=float)
            if raw.ndim != 0 or not np.isfinite(raw) or float(raw) < 0:
                raise ValueError(name + ' must be a finite nonnegative scalar')
            return float(raw)
        relative_cutoff = tolerance(relative_cutoff, 'relative_cutoff')
        absolute_cutoff = tolerance(absolute_cutoff, 'absolute_cutoff')
        support_tolerance = tolerance(support_tolerance, 'support_tolerance')
        scale = float(np.max(np.abs(c))) if c.size else 0.0
        symmetry_threshold = relative_cutoff * scale
        if not math.isfinite(symmetry_threshold):
            raise ValueError('Nonfinite symmetry threshold')
        if not np.allclose(c, c.T, rtol=0, atol=symmetry_threshold):
            raise ValueError('Asymmetric covariance')
        values, vectors = np.linalg.eigh(c*0.5+c.T*0.5)
        largest = max(0.0, float(values[-1])) if values.size else 0.0
        threshold = max(absolute_cutoff, relative_cutoff*largest)
        if not math.isfinite(threshold):
            raise ValueError('Nonfinite eigenvalue threshold')
        if np.any(values < -threshold):
            raise ValueError('Indefinite covariance')
        positive = values > threshold
        return cls(vectors[:,positive], values[positive], vectors[:,~positive],
                   threshold, support_tolerance)

    @property
    def rank(self):
        return int(self.positive_eigenvalues.size)

    def evaluate(self, residual):
        r = np.asarray(residual, dtype=float)
        if r.shape != (self.positive_vectors.shape[0],) or not np.isfinite(r).all():
            raise ValueError('Residual has wrong dimension or nonfinite values')
        null_norm = float(np.linalg.norm(self.null_vectors.T @ r))
        support_ok = null_norm <= self.support_tolerance
        whitened = (self.positive_vectors.T @ r)/np.sqrt(self.positive_eigenvalues)
        chi2 = float(whitened @ whitened)
        log_pdet = float(np.log(self.positive_eigenvalues).sum())
        # Density is relative to Euclidean measure on the support. Absolute
        # values across differently embedded data need their measure/Jacobian.
        log_density = -0.5*(self.rank*math.log(2*math.pi)+log_pdet+chi2)
        return {'rank':self.rank,'nullity':int(self.null_vectors.shape[1]),
                'threshold':self.threshold,'null_residual_norm':null_norm,
                'support_tolerance':self.support_tolerance,'support_ok':bool(support_ok),
                'chi2_pseudoinverse':chi2,
                'log_density':log_density if support_ok else float('-inf')}


def gaussian_prior_marginal(data, mean, covariance, design, prior_mean, prior_covariance):
    """Analytic normalized Gaussian prior integral, not a flat-prior evidence.

    The prior is proper and the residual covariance is fixed. The induced
    support can expand; caller must compare models under one consistent
    observation measure, never densities of unlike-dimensional supports.
    """
    y=np.asarray(data,dtype=float);mu=np.asarray(mean,dtype=float)
    c=np.asarray(covariance,dtype=float);a=np.asarray(design,dtype=float)
    m=np.asarray(prior_mean,dtype=float);s=np.asarray(prior_covariance,dtype=float)
    # Validate every dimension before numpy can broadcast or multiply.
    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError('Observation covariance must be square')
    if s.ndim != 2 or s.shape[0] != s.shape[1]:
        raise ValueError('Prior covariance must be square')
    n, p = c.shape[0], s.shape[0]
    expected = ((y, (n,), 'data'), (mu, (n,), 'mean'),
                (a, (n,p), 'design'), (m, (p,), 'prior_mean'),
                (c, (n,n), 'covariance'), (s, (p,p), 'prior_covariance'))
    for value, shape, name in expected:
        if value.shape != shape or not np.isfinite(value).all():
            raise ValueError(name + ' has wrong dimension or nonfinite values')
    SupportGaussian.from_covariance(c)
    SupportGaussian.from_covariance(s)
    return SupportGaussian.from_covariance(c+a@s@a.T).evaluate(y-mu-a@m)
