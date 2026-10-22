"""Exact GLS sufficient-statistic reduction of the fixed scalar F9 model.

This is a conditional predictive Gaussian sampling model, not a composite-null
supremum, a calibrated beta profile, or permission to open observations.
"""
import math
import numpy as np
from tail_adapter_r2 import CalibrationError, _array, _finite, qualify_gaussian_score


def qualify_scalar_synthetic(spec, values, covariance):
    required = {'id', 'route_id', 'scenario_id', 'mode', 'background_sampling',
                'parameters_fixed_independently_of_y', 'K', 'H_bg', 'sigma_bg', 'covariance_sha256'}
    if not isinstance(spec, dict) or not required <= spec.keys():
        raise CalibrationError('explicit scalar sampling contract required')
    if spec['mode'] != 'SYNTHETIC_ONLY' or spec['background_sampling'] != 'GAUSSIAN_DRAW_IN_SAMPLING_MODEL':
        raise CalibrationError('not qualified for observed/composite background inference')
    if spec['parameters_fixed_independently_of_y'] is not True:
        raise CalibrationError('fixed errors/cosmology/scenario required')
    c = _array(covariance, 'C'); y = _array(values, 'y')
    if y.ndim != 1 or y.size < 2 or c.shape != (len(y), len(y)) or not np.array_equal(c, c.T):
        raise CalibrationError('fixed symmetric multireader covariance required')
    # Canonical matrix bytes make the passed covariance auditable, not guessed.
    import hashlib
    measured = hashlib.sha256(c.astype('<f8').tobytes(order='C')).hexdigest()
    if measured != spec['covariance_sha256']:
        raise CalibrationError('covariance does not match the declared matrix pin')
    k, mu, sb = [_finite(spec[n], n) for n in ('K', 'H_bg', 'sigma_bg')]
    if k <= 0 or sb < 0 or k == 1:
        raise CalibrationError('positive nonidentity K and nonnegative background sigma required')
    try:
        with np.errstate(all='raise'):
            np.linalg.cholesky(c)
            one = np.ones(len(y))
            ci1 = np.linalg.solve(c, one)
            precision = _finite(float(one @ ci1), 'GLS precision')
            if precision <= 0:
                raise CalibrationError('positive precision required')
            local_var = 1 / precision
            h = _finite(float(ci1 @ y / precision), 'GLS statistic')
            residual = y-h*one
            perpendicular = _finite(float(residual @ np.linalg.solve(c, residual)), 'perpendicular Q')
            v0 = _finite(local_var+sb*sb, 'null variance')
            v1 = _finite(local_var+k*k*sb*sb, 'alternative variance')
            gs = {'id': spec['id'], 'route_id': spec['route_id'], 'scenario_id': spec['scenario_id'],
                  'kind': 'SIMPLE_GAUSSIAN_KNOWN_SPD', 'parameters_fixed_independently_of_y': True,
                  'mu0': [mu], 'mu1': [k*mu], 'cov0': [[v0]], 'cov1': [[v1]]}
            q = qualify_gaussian_score(gs, [h])
            ll = qualify_gaussian_score(gs, [h], 'normalized_log_likelihood_ratio')
    except (FloatingPointError, np.linalg.LinAlgError, OverflowError) as ex:
        raise CalibrationError('scalar reduction numeric failure') from ex
    return {'gls_value': h, 'sigma_local_squared': local_var, 'common_perpendicular_Q': perpendicular,
            'null_variance': v0, 'alternative_variance': v1, 'covariance_sha256': measured,
            'score_quadratic_tail': q, 'score_with_logdet_tail': ll,
            'legacy_signed_sqrt_Q_difference': math.copysign(math.sqrt(abs(q['raw_score'])), q['raw_score']),
            'sampling_scope': 'PREDICTIVE_SIMPLE_GAUSSIAN_WITH_FIXED_K_C_H_BG_SIGMA_BG',
            'limitations': ['Not a uniform p over unknown fixed true H0', 'Not beta-profile calibration',
                            'Not local covariances or K estimated using these same observations',
                            'Not multiplicity-adjusted or an observed F9 verdict'],
            'observed_verdict': None, 'gate_moved': False}
