"""Synthetic Gaussian upper-tail bound, robust to covariance and bounded bias.

No data opening or F9 verdict. The caller must independently justify all total
sigmas and the null bias bound. A string naming a source is not its validation.
"""
from fractions import Fraction
import importlib.util
from pathlib import Path
import math

_path=Path(__file__).resolve().parents[1]/'r1_envelope'/'covariance_envelope_r1.py'
_spec=importlib.util.spec_from_file_location('f9_exact_envelope',_path)
_env=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_env)

class RobustTailError(ValueError):pass

def upper_tail(*,contrast,weights,local_sigmas,background_sigma,factor,
               null_bias_upper_bound,bias_source,mode,tests_in_family):
    if mode!='SYNTHETIC_ONLY':raise RobustTailError('SYNTHETIC_ONLY')
    if type(tests_in_family) is not int or tests_in_family<1:
        raise RobustTailError('FINITE_FAMILY_SIZE_REQUIRED')
    if not isinstance(bias_source,str) or not bias_source.strip():
        raise RobustTailError('NAMED_BIAS_BOUND_REQUIRED')
    if null_bias_upper_bound is None:raise RobustTailError('NULL_BIAS_UNBOUNDED')
    try:
        d=_env.rational(contrast);f=_env.rational(factor)
        b=_env.rational(null_bias_upper_bound)
        w=[_env.rational(v) for v in weights]
        if sum(w)!=1:raise RobustTailError('EXACT_NORMALIZED_FIXED_WEIGHTS_REQUIRED')
        if f<=0 or b<0:raise RobustTailError('POSITIVE_FACTOR_NONNEGATIVE_BIAS_BOUND')
        envelope=_env.fixed_contrast_envelope(w+[-f],list(local_sigmas)+[background_sigma])
        radius=envelope['standard_error_bound']
        z=float((d-b)/radius)
        if not math.isfinite(z):raise RobustTailError('UNREPRESENTABLE_STANDARDIZED_CONTRAST')
    except (ValueError,TypeError,OverflowError) as exc:
        if isinstance(exc,RobustTailError):raise
        raise RobustTailError(str(exc)) from exc
    # For negative thresholds, maximal variance need not maximize the tail.
    # Return 1 there rather than extrapolating the positive-tail envelope.
    p=1.0 if d<=b else .5*math.erfc(z/math.sqrt(2))
    if p==0:raise RobustTailError('TAIL_UNDERFLOW_NO_INFINITE_SIGMA')
    return {'p_upper_conservative':p,'p_bonferroni':min(1,tests_in_family*p),
            'contrast_minus_null_bias_over_sd_bound':z,
            'standard_error_bound_exact':[radius.numerator,radius.denominator],
            'scope':'UNIFORM_GAUSSIAN_UPPER_TAIL_WITHIN_DECLARED_TOTAL_SIGMAS_AND_NULL_BIAS_BOUND',
            'covariance_class':'ALL_PSD_WITH_GIVEN_DIAGONAL_INCLUDING_LOCAL_BACKGROUND',
            'sampling_model':'joint Gaussian; fixed weights and factor; fixed unknown H0 cancels',
            'physical_assumptions_verified':False,'observed_F9_verdict':None,
            'numerics':'FLOAT64_ERFC_NOT_INTERVAL_CERTIFICATE'}
