"""Exact-rational variance envelopes; no observations, distribution or verdict.

Input variances are assumed correct TOTAL marginal errors of a common target.
Only a mathematical bound is returned. This code cannot certify that assumption.
"""
from fractions import Fraction
import math


class EnvelopeError(ValueError):
    pass


def rational(x):
    if type(x) is bool or type(x) not in (int, float, Fraction):
        raise EnvelopeError("RATIONAL_NUMERIC_INPUT_REQUIRED")
    if type(x) is float and not math.isfinite(x):
        raise EnvelopeError("NONFINITE_INPUT")
    return Fraction(x)


def fixed_contrast_envelope(coefficients, sigmas):
    if not coefficients or len(coefficients) != len(sigmas):
        raise EnvelopeError("DIMENSION_MISMATCH")
    w, s = list(map(rational, coefficients)), list(map(rational, sigmas))
    if any(x <= 0 for x in s):
        raise EnvelopeError("POSITIVE_TOTAL_MARGINAL_SIGMAS_REQUIRED")
    a = sum(abs(x) * y for x, y in zip(w, s))
    # This rank-one matrix has the stipulated diagonal and attains the bound.
    v = [y if x >= 0 else -y for x, y in zip(w, s)]
    return {"variance_bound": a*a, "standard_error_bound": a,
            "attaining_covariance": [[x*y for y in v] for x in v],
            "physical_covariance_admitted": False, "tail_probability": None}


def mean_minimax_design(sigmas):
    s = list(map(rational, sigmas))
    if not s or any(x <= 0 for x in s):
        raise EnvelopeError("POSITIVE_TOTAL_MARGINAL_SIGMAS_REQUIRED")
    k = min(range(len(s)), key=lambda i: (s[i], i))
    weights = [Fraction(int(i == k)) for i in range(len(s))]
    smallest = s[k]*s[k]
    # A worst covariance for oracle BLUE/GLS as a variational problem; do not
    # confuse it with the rank-one extremizer for every individual fixed w.
    worst = [[smallest + (s[i]*s[i]-smallest if i == j else 0)
              for j in range(len(s))] for i in range(len(s))]
    return {"weights": weights, "selected_index": k,
            "variance_minimax": smallest, "oracle_gls_worst_covariance": worst,
            "selection_uses": "total sigmas and preregistered index tie-break only",
            "physical_covariance_admitted": False, "observed_data_consumed": False}


def quadratic(weights, matrix):
    w = list(map(rational, weights))
    if len(matrix) != len(w) or any(len(r) != len(w) for r in matrix):
        raise EnvelopeError("DIMENSION_MISMATCH")
    return sum(w[i]*rational(matrix[i][j])*w[j]
               for i in range(len(w)) for j in range(len(w)))
