"""Conditional analytic calibration; no F9 verdict, observation, or authorization.

Means/covariances are fixed generative inputs, not fits to y. Numerical tails are
double precision evaluations of analytic laws, not interval certificates.
"""
from dataclasses import dataclass
from statistics import NormalDist
import hashlib
import json
import math
import numpy as np


class CalibrationError(ValueError):
    pass


def _finite(value, label):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise CalibrationError(label + ': finite nonboolean number required')
    value = float(value)
    if not math.isfinite(value):
        raise CalibrationError(label + ': nonfinite number')
    return value


def _array(value, label):
    raw = np.asarray(value, dtype=object)
    values = [_finite(x, label) for x in raw.flat]
    return np.array(values, dtype=float).reshape(raw.shape)


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def _sf(z):
    return .5 * math.erfc(z / math.sqrt(2))


def _interval(lo, hi):
    # Avoid cancellation from 1-Phi(z) at positive z.
    if lo >= 0:
        return _sf(lo) - _sf(hi)
    if hi <= 0:
        return _sf(-hi) - _sf(-lo)
    return 1 - _sf(-lo) - _sf(hi)


def _tail_result(p):
    p = _finite(p, 'tail')
    if not 0 < p <= 1:
        raise CalibrationError('tail zero/underflow/out-of-range: no infinite sigma emitted')
    return {'p_upper': p, 'z_upper_normal_equivalent': -NormalDist().inv_cdf(p) if p < 1 else None,
            'z_limit_if_p_one': '-infinity' if p == 1 else None,
            'numerics': 'FLOAT64_ANALYTIC_EVALUATION_NOT_INTERVAL_CERTIFICATE'}


def qualify_gaussian_score(contract, y, score_kind='quadratic_difference'):
    """Calibrate T=Q0-Q1 or 2(logL1-logL0), upper tail under fixed H0.

    Equal SPD covariances: exact normal law. Unequal scalar variances: exact
    quadratic-normal law by roots. Unequal multivariate: fail closed on p/Z.
    Missing/estimated/composite distributions are never silently accepted.
    """
    if not isinstance(contract, dict):
        raise CalibrationError('explicit generative contract required')
    required = {'id', 'route_id', 'scenario_id', 'kind', 'parameters_fixed_independently_of_y', 'mu0', 'mu1', 'cov0', 'cov1'}
    if not required <= contract.keys():
        raise CalibrationError('missing contract fields: ' + str(sorted(required - contract.keys())))
    if any(not isinstance(contract[k], str) or not contract[k].strip() for k in ['id', 'route_id', 'scenario_id']):
        raise CalibrationError('named contract/route/scenario required')
    if contract['kind'] != 'SIMPLE_GAUSSIAN_KNOWN_SPD' or contract['parameters_fixed_independently_of_y'] is not True:
        raise CalibrationError('only explicitly fixed simple Gaussian generative models qualified')
    if score_kind not in ('quadratic_difference', 'normalized_log_likelihood_ratio'):
        raise CalibrationError('sqrtDeltaQ/lnB cannot be used as calibrated p or sigma')
    m0, m1, yy = [_array(v, 'vector') for v in (contract['mu0'], contract['mu1'], y)]
    s0, s1 = [_array(v, 'covariance') for v in (contract['cov0'], contract['cov1'])]
    if m0.ndim != 1 or m0.size == 0 or m1.shape != m0.shape or yy.shape != m0.shape:
        raise CalibrationError('incompatible vector dimensions')
    n = len(m0)
    for s in (s0, s1):
        if s.shape != (n, n) or not np.array_equal(s, s.T):
            raise CalibrationError('exact symmetric covariance shape required; no repair')
        try:
            np.linalg.cholesky(s)
        except np.linalg.LinAlgError as ex:
            raise CalibrationError('positive definite covariance required') from ex
    try:
        with np.errstate(all='raise'):
            l0 = np.linalg.cholesky(s0)
            delta = m1 - m0
            q0 = float((yy-m0) @ np.linalg.solve(s0, yy-m0))
            q1 = float((yy-m1) @ np.linalg.solve(s1, yy-m1))
            constant = 0.0 if score_kind == 'quadratic_difference' else float(np.linalg.slogdet(s0)[1] - np.linalg.slogdet(s1)[1])
            score = _finite(q0-q1+constant, 'score')
            a = np.eye(n) - l0.T @ np.linalg.solve(s1, l0)
            b = 2 * l0.T @ np.linalg.solve(s1, delta)
            c = float(-delta @ np.linalg.solve(s1, delta)+constant)
            _array(a, 'quadratic coefficient'); _array(b, 'linear coefficient'); _finite(c, 'constant')
    except (FloatingPointError, np.linalg.LinAlgError, OverflowError) as ex:
        raise CalibrationError('nonfinite/ill-conditioned numeric operation') from ex
    out = {'contract_id': contract['id'], 'contract_sha256': _digest(contract), 'route_id': contract['route_id'],
           'scenario_id': contract['scenario_id'], 'score_kind': score_kind, 'raw_score': score,
           'scope': 'CONDITIONAL_ON_FIXED_SIMPLE_GENERATIVE_MODEL_NOT_F9_OBSERVED',
           'null_quadratic_form': {'A': a.tolist(), 'b': b.tolist(), 'c': c},
           'p_upper': None, 'z_upper_normal_equivalent': None}
    if np.array_equal(s0, s1):
        d2 = _finite(float(delta @ np.linalg.solve(s0, delta)), 'D_squared')
        if d2 <= 0:
            raise CalibrationError('identical/degenerate hypotheses: no normal separation calibration')
        z = (score+d2)/(2*math.sqrt(d2))
        out.update(_tail_result(_sf(z)))
        out.update(calibration='ANALYTIC_SIMPLE_NORMAL', null_mean=-d2, null_variance=4*d2, design_D=math.sqrt(d2))
        return out
    if n != 1:
        out.update(calibration='CALIBRATION_UNAVAILABLE', reason='GENERALIZED_QUADRATIC_NORMAL_CDF_NOT_QUALIFIED')
        return out
    # Scalar whitening gives a Z²+b Z+c. Complete the square; do not use Wilks.
    av, bv = float(a[0, 0]), float(b[0])
    if av == 0:
        raise CalibrationError('unequal covariance rounded to zero quadratic coefficient')
    center = -bv/(2*av)
    radius2 = (score-c)/av + center*center
    _finite(center, 'quadratic center'); _finite(radius2, 'quadratic radius squared')
    if radius2 <= 0:
        p = 1.0 if av > 0 else 0.0
    else:
        radius = math.sqrt(radius2)
        lo, hi = center-radius, center+radius
        p = _sf(-lo)+_sf(hi) if av > 0 else _interval(lo, hi)
    out.update(_tail_result(p))
    out.update(calibration='ANALYTIC_SCALAR_QUADRATIC_NORMAL', root_center=center, root_radius_squared=radius2)
    return out


def adjust_family(contract, records):
    """Finite named family/scenarios only; no default five-test F9 family.

    Records are trusted outputs from qualify_gaussian_score, not certificates
    authenticating a caller. Contract choices require a separate frozen act.
    """
    required = {'id', 'route_id', 'method', 'test_ids', 'scenario_ids', 'scope'}
    if not isinstance(contract, dict) or not required <= contract.keys():
        raise CalibrationError('explicit multiplicity contract required')
    if contract['scope'] != 'SYNTHETIC_QUALIFICATION_ONLY':
        raise CalibrationError('observed/frozen family adoption is not authorized by this component')
    method = contract['method']
    if method not in ('bonferroni', 'none_single_test'):
        raise CalibrationError('Sidak/other method requires separate dependence qualification')
    tests, scenarios = contract['test_ids'], contract['scenario_ids']
    for values in (tests, scenarios):
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values) or len(set(values)) != len(values):
            raise CalibrationError('nonempty unique test/scenario IDs required')
    if method == 'none_single_test' and len(tests) != 1:
        raise CalibrationError('no multiplicity correction only for one test')
    expected = {(t, s) for t in tests for s in scenarios}
    if not isinstance(records, list):
        raise CalibrationError('records must be a list')
    seen = {}
    for item in records:
        if not isinstance(item, dict) or not {'test_id', 'result'} <= item.keys() or not isinstance(item['result'], dict):
            raise CalibrationError('invalid calibrated record')
        r = item['result']; key = (item['test_id'], r.get('scenario_id'))
        if key not in expected or key in seen or r.get('route_id') != contract['route_id']:
            raise CalibrationError('unexpected/duplicate/cross-route scenario')
        if r.get('calibration') not in ('ANALYTIC_SIMPLE_NORMAL', 'ANALYTIC_SCALAR_QUADRATIC_NORMAL'):
            raise CalibrationError('missing distribution/calibration; no subset robust p')
        p = _finite(r.get('p_upper'), 'p')
        if not 0 < p <= 1:
            raise CalibrationError('invalid tail')
        seen[key] = p
    if set(seen) != expected:
        raise CalibrationError('incomplete frozen family/scenarios')
    result = {}
    m = len(tests)
    for t in tests:
        robust = max(seen[t, s] for s in scenarios)
        adjusted = min(1.0, m*robust) if method == 'bonferroni' else robust
        result[t] = {'p_robust': robust, 'multiplicity_factor': m, **_tail_result(adjusted)}
    return {'contract_sha256': _digest(contract), 'route_id': contract['route_id'], 'method': method,
            'dependence_scope': 'BONFERRONI_VALID_UNDER_ARBITRARY_TEST_DEPENDENCE_IF_EACH_NULL_P_VALID',
            'scenario_scope': 'UNION_OF_EXPLICIT_FINITE_SCENARIOS_ONLY_NOT_CONTINUOUS_NUISANCE_SUPREMUM',
            'results': result, 'observed_verdict': None, 'gate_moved': False}
