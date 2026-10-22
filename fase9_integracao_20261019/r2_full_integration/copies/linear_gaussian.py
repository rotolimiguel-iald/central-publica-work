"""Common flat-nuisance integral on a fixed Gaussian support.

No data access, optimization, priors or cosmology are implicit in this module.
The caller must freeze observation units, support tolerances and a common
Lebesgue nuisance measure before comparing relative evidences.
"""
import math
import numpy as np
from singular_gaussian_v2 import SupportGaussian


class FlatNuisanceGaussian:
    def __init__(self, covariance, design, *, relative_cutoff=1e-12,
                 absolute_cutoff=0.0, support_tolerance=1e-10,
                 design_relative_cutoff=1e-12):
        self.support = SupportGaussian.from_covariance(
            covariance, relative_cutoff, absolute_cutoff, support_tolerance)
        self.n = self.support.positive_vectors.shape[0]
        x = np.asarray(design, dtype=float)
        if x.ndim != 2 or x.shape[0] != self.n or not np.isfinite(x).all():
            raise ValueError('Invalid nuisance design')
        if not np.isscalar(design_relative_cutoff) or not np.isfinite(design_relative_cutoff) or not 0 <= design_relative_cutoff < 1:
            raise ValueError('Invalid design relative cutoff')
        self.p = x.shape[1]
        if self.p > self.support.rank:
            raise ValueError('More flat nuisance columns than supported directions')
        self._check_supported_columns(x)
        self.whitener = (self.support.positive_vectors / np.sqrt(
            self.support.positive_eigenvalues)).T
        xw = self.whitener @ x
        u, s, _ = np.linalg.svd(xw, full_matrices=False)
        if not np.isfinite(s).all() or (self.p and np.any(s <= design_relative_cutoff*s[0])):
            raise ValueError('Unidentified or ill-conditioned flat nuisance direction')
        self.q = u
        self.design_singular_values = s
        self.log_det_information = float(2*np.log(s).sum())
        self.log_prefactor = -0.5*((self.support.rank-self.p)*math.log(2*math.pi)
            + np.log(self.support.positive_eigenvalues).sum()
            + self.log_det_information)
        if not np.isfinite(self.log_prefactor):
            raise ValueError('Nonfinite normalization')

    def _check_supported_columns(self, matrix):
        errors = np.linalg.norm(self.support.null_vectors.T @ matrix, axis=0)
        if np.any(errors > self.support.support_tolerance):
            raise ValueError('Design or response lies outside covariance support')

    def residualize(self, matrix):
        a = np.asarray(matrix, dtype=float)
        if a.ndim != 2 or a.shape[0] != self.n or not np.isfinite(a).all():
            raise ValueError('Invalid response matrix')
        self._check_supported_columns(a)
        aw = self.whitener @ a
        return aw-self.q@(self.q.T@aw)

    def response_information(self, matrix):
        """Error/design-only information; no observed residual is consumed."""
        t = self.residualize(matrix)
        result = t.T@t
        if not np.isfinite(result).all():
            raise ValueError('Nonfinite response information')
        return result

    def log_integral(self, data_minus_physical_mean):
        """Log integral d(eta); an arbitrary common measure constant is omitted.

        This is not an absolute Bayesian evidence. All model-specific priors
        still have to be proper, and model comparisons require the same support.
        """
        b = np.asarray(data_minus_physical_mean, dtype=float)
        check = self.support.evaluate(b)
        if not check['support_ok']:
            return float('-inf')
        bw = self.whitener@b
        remainder = bw-self.q@(self.q.T@bw)
        value = float(self.log_prefactor-0.5*(remainder@remainder))
        if not np.isfinite(value):
            raise ValueError('Nonfinite flat integral inside support')
        return value
